import os, csv, zipfile, sqlite3, requests
from typing import Tuple, List, Optional

# Reuse your app's data dir (adjust import if your path differs)
try:
    from db import DATA_DIR
except Exception:
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

API_BASE = "https://api.company-information.service.gov.uk"
KEY_FILE = os.path.join(DATA_DIR, "companies_house_api_key.txt")

# Offline data files (put one of these in data/)
OFFLINE_CSV = os.path.join(DATA_DIR, "ch_basic_company_data.csv")
OFFLINE_ZIP = os.path.join(DATA_DIR, "ch_basic_company_data.zip")

# SQLite table to store an index of (company_number -> company_name, status)
OFFLINE_TABLE = "ch_company_index"
OFFLINE_DB = os.path.join(DATA_DIR, "mse.db")  # same DB as the app

# ---------- Common helpers ----------

def _normalize_name(s: str) -> str:
    s = (s or "").strip().upper()
    # Replace quotes with spaces to preserve word boundaries (e.g., "APS"HANDYBUILDER -> APS HANDYBUILDER)
    s = s.replace('"', ' ').replace("'", ' ')
    for token in (" LIMITED", " LTD", " PLC", " INC", " LLC"):
        if s.endswith(token): s = s[: -len(token)]
    for t in (".", ",", "&", " AND "):
        s = s.replace(t, " ")
    return " ".join(s.split())

def _api_key() -> Optional[str]:
    # Prefer env var; fallback to data/companies_house_api_key.txt
    key = os.environ.get("COMPANIES_HOUSE_API_KEY", "").strip()
    if not key and os.path.exists(KEY_FILE):
        # utf-8-sig strips a BOM if present
        with open(KEY_FILE, "r", encoding="utf-8-sig") as f:
            key = f.read().strip()
    return key or None

def save_api_key(key: str) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        f.write((key or "").strip())

def _auth():
    k = _api_key()
    if not k:
        return None  # indicates offline-only
    return (k, "")

# ---------- ONLINE (live API) ----------

def _get_company_by_number_online(company_no: str) -> dict | None:
    a = _auth()
    if a is None:
        raise RuntimeError("NO_API_KEY")  # signal to the caller to use offline
    r = requests.get(f"{API_BASE}/company/{company_no}", auth=a, timeout=10)
    if r.status_code == 200: return r.json()
    if r.status_code == 404: return None
    if r.status_code == 401:
        raise RuntimeError("BAD_API_KEY")  # explicit 401
    r.raise_for_status()

def _search_by_name_online(name: str, items: int = 10) -> dict:
    a = _auth()
    if a is None:
        raise RuntimeError("NO_API_KEY")
    r = requests.get(
        f"{API_BASE}/search/companies",
        params={"q": name, "items_per_page": items},
        auth=a,
        timeout=10,
    )
    if r.status_code == 200: return r.json()
    if r.status_code == 401:
        raise RuntimeError("BAD_API_KEY")
    r.raise_for_status()

# ---------- OFFLINE (bulk CSV/ZIP) ----------

def _connect() -> sqlite3.Connection:
    con = sqlite3.connect(OFFLINE_DB)
    con.row_factory = sqlite3.Row
    return con

def _offline_table_exists(con: sqlite3.Connection) -> bool:
    row = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (OFFLINE_TABLE,)).fetchone()
    return row is not None

def _rows_from_csv_like() -> csv.DictReader:
    # Open CSV directly or first CSV inside the ZIP
    if os.path.exists(OFFLINE_CSV):
        f = open(OFFLINE_CSV, "r", encoding="utf-8", newline="")
        return csv.DictReader(f)
    if os.path.exists(OFFLINE_ZIP):
        zf = zipfile.ZipFile(OFFLINE_ZIP, "r")
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_names:
            raise FileNotFoundError("ZIP file has no CSV inside.")
        # open as text
        f = zf.open(csv_names[0], "r")
        return csv.DictReader((line.decode("utf-8", "ignore") for line in f))
    raise FileNotFoundError(
        "Offline dataset not found. Place 'ch_basic_company_data.csv' or 'ch_basic_company_data.zip' in the data/ folder."
    )

def _seed_offline_index_if_needed() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with _connect() as con:
        if _offline_table_exists(con):
            return
        # Build the table
        con.execute(f"CREATE TABLE {OFFLINE_TABLE} (company_number TEXT PRIMARY KEY, company_name TEXT, status TEXT)")
        con.execute(f"CREATE INDEX IF NOT EXISTS idx_{OFFLINE_TABLE}_num ON {OFFLINE_TABLE}(company_number)")
        batch, n = [], 0
        reader = _rows_from_csv_like()
        # Flexible column names
        headers = {h.strip().lower(): h for h in reader.fieldnames or []}
        cn_key = headers.get("companynumber") or headers.get("company number") or "CompanyNumber"
        name_key = headers.get("companyname") or headers.get("company name") or "CompanyName"
        status_key = headers.get("companystatus") or headers.get("company status") or "CompanyStatus"

        for row in reader:
            num = (row.get(cn_key) or "").strip().upper()  # Store in uppercase for case-insensitive matching
            if not num: continue
            name = (row.get(name_key) or "").strip()
            status = (row.get(status_key) or "").strip()
            batch.append((num, name, status))
            if len(batch) >= 10000:
                con.executemany(f"INSERT OR REPLACE INTO {OFFLINE_TABLE}(company_number, company_name, status) VALUES(?,?,?)", batch)
                con.commit(); batch.clear()
                n += 10000
        if batch:
            con.executemany(f"INSERT OR REPLACE INTO {OFFLINE_TABLE}(company_number, company_name, status) VALUES(?,?,?)", batch)
            con.commit()
        # Optional: print to console so you see progress once
        print(f"[CH-OFFLINE] Indexed basic company data into SQLite table '{OFFLINE_TABLE}'.")

def _verify_offline(name: str, company_no: str) -> Tuple[bool, List[str]]:
    _seed_offline_index_if_needed()
    with _connect() as con:
        # Convert company number to uppercase for case-insensitive matching
        rec = con.execute(f"SELECT company_name FROM {OFFLINE_TABLE} WHERE company_number=?", (company_no.upper(),)).fetchone()
        if not rec:
            return False, ["Invalid company number (not found in offline dataset)."]
        ch_name = rec["company_name"] or ""
        normalized_ch_name = _normalize_name(ch_name)
        normalized_input_name = _normalize_name(name)

        # Allow flexible matching:
        # 1. Input matches the beginning of the company name (partial match)
        # 2. Input exactly matches the full company name
        if normalized_ch_name.startswith(normalized_input_name) or normalized_ch_name == normalized_input_name:
            return True, []

        return False, ["Company name does not match the offline Companies House dataset for that number."]

# ---------- Unified entry point used by your UI ----------

def verify_company_against_ch(name: str, company_no: str) -> Tuple[bool, List[str]]:
    """
    Attempts live Companies House REST API if a key is present; otherwise falls back to the
    offline bulk dataset (no authorization required).
    Returns (ok, messages).
    """
    # Try online first if key present
    if _api_key():
        try:
            # Use uppercase company number for consistent case-insensitive matching
            rec = _get_company_by_number_online(company_no.upper())
            if not rec:
                return False, ["Invalid company number (not found on Companies House)."]
            # also confirm the name exists in search results
            search = _search_by_name_online(name, items=10)
            if not (search and search.get("items")):
                return False, ["Invalid company name (no matching name on Companies House)."]
            ch_name = rec.get("company_name", "")
            normalized_ch_name = _normalize_name(ch_name)
            normalized_input_name = _normalize_name(name)

            # Allow flexible matching: partial or full
            if normalized_ch_name.startswith(normalized_input_name) or normalized_ch_name == normalized_input_name:
                return True, []

            return False, ["Company name does not match the Companies House record for that number."]
        except RuntimeError as e:
            # BAD_API_KEY or NO_API_KEY -> just drop to offline
            if str(e) not in ("BAD_API_KEY", "NO_API_KEY"):
                return False, [f"Companies House error: {e}"]
        except requests.RequestException as e:
            # Network hiccup -> fallback offline
            pass
        except Exception as e:
            # Any other HTTP parsing issue -> fallback offline
            pass

    # Offline fallback (no key needed)
    try:
        return _verify_offline(name, company_no)
    except FileNotFoundError as e:
        # No offline dataset present
        return False, [
            "Could not verify company: no API key and no offline dataset found.",
            "Either add a REST API key (data/companies_house_api_key.txt) OR place "
            "'ch_basic_company_data.csv' (or .zip) in the data/ folder."
        ]
    except Exception as e:
        return False, [f"Offline verification failed: {e}"]