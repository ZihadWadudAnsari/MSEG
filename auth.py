import os, hashlib
from db import DATA_DIR, ensure_dirs, company_by_reg_no, company_insert, company_get

USERS_FILE = os.path.join(DATA_DIR, "users.txt")

def sha256(txt: str) -> str:
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()

def ensure_users_file():
    ensure_dirs()
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        demo_company = company_by_reg_no("REGDEMO1")
        if not demo_company:
            cid = company_insert("Demo Company Ltd", "REGDEMO1", "2010-01-01", 1)
        else:
            cid = demo_company["company_id"]
        demo = [
            f"stock_manager|manager1|{sha256('pass123')}",
            f"company|company1|{sha256('pass456')}|{cid}",
        ]
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(demo))

def parse_users_file():
    users = []
    if not os.path.exists(USERS_FILE): return users
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) not in (3,4): continue
            item = {"role": parts[0].lower(), "username": parts[1].lower(), "hash": parts[2]}
            item["company_id"] = int(parts[3]) if len(parts)==4 and parts[3].isdigit() else None
            users.append(item)
    return users

def username_taken(username: str) -> bool:
    u = username.lower().strip()
    return any(x["username"] == u for x in parse_users_file())

def add_company_login(username: str, password: str, company_id: int):
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + f"company|{username}|{sha256(password)}|{company_id}")

def verify_credentials(role: str, username: str, password: str):
    role = role.lower().strip()
    uname = username.lower().strip()
    h = sha256(password)
    for rec in parse_users_file():
        if rec["role"] == role and rec["username"] == uname and rec["hash"] == h:
            company_id = rec.get("company_id")
            if rec["role"] == "company" and company_id:
                try:
                    if not company_get(company_id):
                        company_id = None
                except Exception:
                    company_id = None
            return {"role": rec["role"], "username": uname, "company_id": company_id}
    return None
