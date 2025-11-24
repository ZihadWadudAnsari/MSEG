import os, sqlite3, shutil, re, time, random
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")
DB_PATH = os.path.join(DATA_DIR, "mse.db")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON;")
    return con

DDL = [
    '''
    CREATE TABLE IF NOT EXISTS sector (
        sector_id   INTEGER PRIMARY KEY,
        sector_name TEXT NOT NULL
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS company (
        company_id         INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name       TEXT NOT NULL,
        registration_no    TEXT NOT NULL UNIQUE,
        incorporation_date TEXT NOT NULL,
        sector_id          INTEGER NOT NULL,
        FOREIGN KEY(sector_id) REFERENCES sector(sector_id) ON DELETE RESTRICT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS application (
        application_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id         INTEGER NOT NULL,
        application_date   TEXT NOT NULL,
        proposed_ticker    TEXT NOT NULL,
        proposed_shares    INTEGER NOT NULL CHECK(proposed_shares > 0),
        proposed_valuation INTEGER NOT NULL CHECK(proposed_valuation > 0),
        status             TEXT NOT NULL DEFAULT 'pending' CHECK(status IN('pending','approved','rejected')),
        rejection_note     TEXT,
        internal_notes     TEXT,
        FOREIGN KEY(company_id) REFERENCES company(company_id) ON DELETE CASCADE
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS stock (
        stock_id           INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id         INTEGER NOT NULL,
        application_id     INTEGER NOT NULL UNIQUE,
        ticker             TEXT NOT NULL UNIQUE,
        shares_outstanding INTEGER NOT NULL CHECK(shares_outstanding > 0),
        valuation          INTEGER NOT NULL CHECK(valuation > 0),
        sector_id          INTEGER NOT NULL,
        listing_date       TEXT NOT NULL,
        FOREIGN KEY(company_id) REFERENCES company(company_id),
        FOREIGN KEY(application_id) REFERENCES application(application_id),
        FOREIGN KEY(sector_id) REFERENCES sector(sector_id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS stock_price (
        price_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_id    INTEGER NOT NULL,
        price_date  TEXT NOT NULL,
        price       REAL NOT NULL,
        FOREIGN KEY(stock_id) REFERENCES stock(stock_id) ON DELETE CASCADE,
        UNIQUE(stock_id, price_date)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS attachment (
        attachment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id  INTEGER NOT NULL,
        filename        TEXT NOT NULL,
        stored_path     TEXT NOT NULL,
        uploaded_at     TEXT NOT NULL,
        FOREIGN KEY(application_id) REFERENCES application(application_id) ON DELETE CASCADE
    );
    '''
]

SECTORS = [
    (1, "Technology"),
    (2, "Telecommunications"),
    (3, "Health Care"),
    (4, "Financials"),
    (5, "Real Estate"),
    (6, "Consumer Discretionary"),
    (7, "Consumer Staples"),
    (8, "Industrials"),
    (9, "Basic Materials"),
    (10, "Energy")
]

def _ensure_app_columns(con: sqlite3.Connection):
    cols = {r["name"] for r in con.execute("PRAGMA table_info(application)")}
    if "internal_notes" not in cols:
        con.execute("ALTER TABLE application ADD COLUMN internal_notes TEXT")

def _ensure_stock_columns(con: sqlite3.Connection):
    cols = {r["name"] for r in con.execute("PRAGMA table_info(stock)")}
    if "sector_id" not in cols:
        con.execute("ALTER TABLE stock ADD COLUMN sector_id INTEGER")
    if "listing_date" not in cols:
        con.execute("ALTER TABLE stock ADD COLUMN listing_date TEXT")

def ensure_db():
    ensure_dirs()
    with db() as con:
        for stmt in DDL:
            con.execute(stmt)
        _ensure_app_columns(con)
        _ensure_stock_columns(con)
        cur = con.execute("SELECT COUNT(*) AS c FROM sector")
        if cur.fetchone()["c"] == 0:
            con.executemany("INSERT INTO sector(sector_id, sector_name) VALUES(?,?)", SECTORS)
            con.commit()

def sectors_all():
    with db() as con:
        return con.execute("SELECT sector_id, sector_name FROM sector ORDER BY sector_id").fetchall()

def company_insert(company_name, reg_no, inc_date_iso, sector_id) -> int:
    with db() as con:
        cur = con.execute(
            "INSERT INTO company(company_name, registration_no, incorporation_date, sector_id) VALUES(?,?,?,?)",
            (company_name, reg_no, inc_date_iso, sector_id)
        )
        con.commit()
        return cur.lastrowid

def company_by_reg_no(reg_no):
    with db() as con:
        return con.execute("SELECT * FROM company WHERE registration_no=?", (reg_no,)).fetchone()

def company_get(company_id):
    with db() as con:
        return con.execute("SELECT * FROM company WHERE company_id=?", (company_id,)).fetchone()

def application_insert(company_id, app_date_iso, ticker, shares, valuation) -> int:
    with db() as con:
        cur = con.execute(
            "INSERT INTO application(company_id, application_date, proposed_ticker, proposed_shares, proposed_valuation) VALUES(?,?,?,?,?)",
            (company_id, app_date_iso, ticker, shares, valuation)
        )
        con.commit()
        return cur.lastrowid

def applications_for_company(company_id):
    with db() as con:
        return con.execute(
            "SELECT * FROM application WHERE company_id=? ORDER BY application_date DESC, application_id DESC",
            (company_id,)
        ).fetchall()

def applications_all():
    with db() as con:
        return con.execute("SELECT * FROM application ORDER BY application_date DESC, application_id DESC").fetchall()

def applications_pending_all():
    with db() as con:
        return con.execute(
            "SELECT * FROM application WHERE status='pending' ORDER BY application_date DESC, application_id DESC"
        ).fetchall()

def application_get(application_id):
    with db() as con:
        return con.execute("SELECT * FROM application WHERE application_id=?", (application_id,)).fetchone()

def application_set_rejected(application_id, note):
    with db() as con:
        con.execute("UPDATE application SET status='rejected', rejection_note=? WHERE application_id=?",
                    (note, application_id))
        con.commit()

def application_set_approved(application_id: int):
    with db() as con:
        con.execute("UPDATE application SET status='approved' WHERE application_id=?", (application_id,))
        con.commit()

# ---------------- Stock Management ----------------

def stock_create_from_application(application_id: int) -> int:
    """Create a stock entry from an approved application and generate 365 days of price history."""
    with db() as con:
        app = con.execute("SELECT * FROM application WHERE application_id=?", (application_id,)).fetchone()
        if not app:
            raise ValueError("Application not found")
        
        # Check if stock already exists
        existing = con.execute("SELECT stock_id FROM stock WHERE application_id=?", (application_id,)).fetchone()
        if existing:
            return existing["stock_id"]
        
        # Get company sector
        company = con.execute("SELECT sector_id FROM company WHERE company_id=?", (app["company_id"],)).fetchone()
        sector_id = company["sector_id"] if company else 1
        
        # Calculate initial price
        initial_price = app["proposed_valuation"] / app["proposed_shares"]
        listing_date = datetime.now().date().isoformat()
        
        # Create stock entry
        cur = con.execute(
            "INSERT INTO stock(company_id, application_id, ticker, shares_outstanding, valuation, sector_id, listing_date) VALUES(?,?,?,?,?,?,?)",
            (app["company_id"], application_id, app["proposed_ticker"], app["proposed_shares"], app["proposed_valuation"], sector_id, listing_date)
        )
        stock_id = cur.lastrowid
        
        # Generate 365 days of historical prices
        current_price = initial_price
        current_date = datetime.now().date()
        
        prices = []
        for i in range(365, -1, -1):  # Go backwards from 365 days ago to today
            price_date = (current_date - timedelta(days=i)).isoformat()
            
            if i < 365:  # Don't change price on first day
                # Random return between -1.5% and +1.5%
                return_pct = random.uniform(-0.015, 0.015)
                current_price = current_price * (1 + return_pct)
                current_price = max(0.01, current_price)  # Ensure price stays positive
            
            prices.append((stock_id, price_date, round(current_price, 2)))
        
        con.executemany(
            "INSERT OR REPLACE INTO stock_price(stock_id, price_date, price) VALUES(?,?,?)",
            prices
        )
        con.commit()
        
        return stock_id

def stocks_all():
    """Get all stocks with their current prices and sector information."""
    with db() as con:
        return con.execute("""
            SELECT s.*, sect.sector_name,
                   (SELECT price FROM stock_price WHERE stock_id = s.stock_id 
                    ORDER BY price_date DESC LIMIT 1) as current_price
            FROM stock s
            LEFT JOIN sector sect ON s.sector_id = sect.sector_id
            ORDER BY s.ticker
        """).fetchall()

def stock_delete(stock_id: int):
    """Delete a stock and its price history."""
    with db() as con:
        con.execute("DELETE FROM stock WHERE stock_id=?", (stock_id,))
        con.commit()

def stock_get_prices(stock_id: int, days: int = None):
    """Get price history for a stock. If days is None, get all prices."""
    with db() as con:
        if days:
            cutoff = (datetime.now().date() - timedelta(days=days)).isoformat()
            return con.execute(
                "SELECT * FROM stock_price WHERE stock_id=? AND price_date >= ? ORDER BY price_date",
                (stock_id, cutoff)
            ).fetchall()
        else:
            return con.execute(
                "SELECT * FROM stock_price WHERE stock_id=? ORDER BY price_date",
                (stock_id,)
            ).fetchall()

def stock_get_current_price(stock_id: int) -> float:
    """Get the most recent price for a stock."""
    with db() as con:
        row = con.execute(
            "SELECT price FROM stock_price WHERE stock_id=? ORDER BY price_date DESC LIMIT 1",
            (stock_id,)
        ).fetchone()
        return row["price"] if row else 0.0

def stock_calculate_return(stock_id: int, days: int) -> float:
    """Calculate return percentage over the last N days."""
    prices = stock_get_prices(stock_id, days + 1)
    if len(prices) < 2:
        return 0.0
    
    start_price = prices[0]["price"]
    end_price = prices[-1]["price"]
    
    if start_price == 0:
        return 0.0
    
    return ((end_price - start_price) / start_price) * 100

def stock_calculate_24hr_change(stock_id: int) -> float:
    """Calculate 24 hour price change percentage."""
    with db() as con:
        # Get last 2 prices
        prices = con.execute(
            "SELECT price FROM stock_price WHERE stock_id=? ORDER BY price_date DESC LIMIT 2",
            (stock_id,)
        ).fetchall()
        
        if len(prices) < 2:
            return 0.0
        
        current = prices[0]["price"]
        previous = prices[1]["price"]
        
        if previous == 0:
            return 0.0
        
        return ((current - previous) / previous) * 100

# ---------------- Attachments + Internal notes ----------------

def _safe_name(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', name)

def attachment_store_from_path(application_id: int, src_path: str) -> int:
    """Copy a file into data/uploads/app_<id>/ and record it in DB."""
    app_dir = os.path.join(UPLOADS_DIR, f"app_{application_id}")
    os.makedirs(app_dir, exist_ok=True)

    base = os.path.basename(src_path)
    base_safe = _safe_name(base)
    stamp = int(time.time() * 1000)
    dest_abs = os.path.join(app_dir, f"{stamp}_{base_safe}")

    shutil.copy2(src_path, dest_abs)
    rel = os.path.relpath(dest_abs, DATA_DIR)

    with db() as con:
        cur = con.execute(
            "INSERT INTO attachment(application_id, filename, stored_path, uploaded_at) VALUES(?,?,?,?)",
            (application_id, base, rel, datetime.now().isoformat(timespec="seconds"))
        )
        con.commit()
        return cur.lastrowid

def attachments_for_application(application_id: int):
    with db() as con:
        return con.execute(
            "SELECT attachment_id, filename, stored_path, uploaded_at FROM attachment "
            "WHERE application_id=? ORDER BY attachment_id",
            (application_id,)
        ).fetchall()

def attachment_abs_path(stored_path: str) -> str:
    return stored_path if os.path.isabs(stored_path) else os.path.join(DATA_DIR, stored_path)

def application_set_internal_notes(application_id: int, notes: str):
    with db() as con:
        con.execute("UPDATE application SET internal_notes=? WHERE application_id=?", (notes, application_id))
        con.commit()