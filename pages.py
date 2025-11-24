import os, re, shutil, sys, subprocess
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
from datetime import date, datetime

from companies_house import verify_company_against_ch, save_api_key
from ui_components import set_widget_colors
from db import (
    db, sectors_all, company_insert, application_insert,
    applications_for_company, application_get,
    applications_pending_all, applications_all,  # ADD applications_all HERE
    application_set_rejected, application_set_approved,
    attachments_for_application, attachment_store_from_path, attachment_abs_path,
    application_set_internal_notes, stock_create_from_application
)
from auth import username_taken, add_company_login

# ----- helper to open files -----
def _open_file_with_os(path: str):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("Open failed", str(e))

# ================= Inline Company Signup =================
class InlineCompanySignup(tk.Frame):
    def __init__(self, master, get_theme, on_success):
        super().__init__(master, bd=1, relief="solid")
        self.get_theme = get_theme
        self.on_success = on_success

        r = 0
        tk.Label(self, text="Company Sign Up", font=("Segoe UI", 12, "bold")).grid(row=r, column=0, columnspan=2, sticky="w", padx=16, pady=(12,4)); r+=1
        tk.Label(self, text="Company Name *").grid(row=r, column=0, sticky="w", pady=4, padx=(16,6))
        self.e_name = tk.Entry(self, width=30); self.e_name.grid(row=r, column=1, sticky="ew", pady=4, padx=(6,16)); r+=1

        tk.Label(self, text="Registration No *").grid(row=r, column=0, sticky="w", pady=4, padx=(16,6))
        self.e_reg = tk.Entry(self); self.e_reg.grid(row=r, column=1, sticky="ew", pady=4, padx=(6,16)); r+=1

        tk.Label(self, text="Incorporation Date * (YYYY-MM-DD)").grid(row=r, column=0, sticky="w", pady=4, padx=(16,6))
        self.e_date = tk.Entry(self); self.e_date.insert(0, "2000-01-01"); self.e_date.grid(row=r, column=1, sticky="ew", pady=4, padx=(6,16)); r+=1

        tk.Label(self, text="Sector *").grid(row=r, column=0, sticky="w", pady=4, padx=(16,6))
        self.sector_opts = [(row["sector_id"], row["sector_name"]) for row in sectors_all()]
        self.cbo_sector = ttk.Combobox(self, state="readonly",
                                       values=[f"{sid} - {name}" for sid, name in self.sector_opts], width=28)
        if self.sector_opts: self.cbo_sector.current(0)
        self.cbo_sector.grid(row=r, column=1, sticky="ew", pady=4, padx=(6,16)); r+=1

        ttk.Separator(self, orient="horizontal").grid(row=r, column=0, columnspan=2, sticky="ew", pady=(8,6)); r+=1

        tk.Label(self, text="Create Login Username *").grid(row=r, column=0, sticky="w", pady=4, padx=(16,6))
        self.e_user = tk.Entry(self); self.e_user.grid(row=r, column=1, sticky="ew", pady=4, padx=(6,16)); r+=1

        tk.Label(self, text="Create Login Password *").grid(row=r, column=0, sticky="w", pady=4, padx=(16,6))
        self.e_pass = tk.Entry(self, show="*"); self.e_pass.grid(row=r, column=1, sticky="ew", pady=4, padx=(6,16)); r+=1

        btns = tk.Frame(self); btns.grid(row=r, column=0, columnspan=2, sticky="e", padx=16, pady=(8,12))
        self.b_ok = tk.Button(btns, text="Create Company", width=16, command=self.do_signup); self.b_ok.pack(side="right", padx=(6,0))
        self.b_cancel = tk.Button(btns, text="Hide", width=10, command=self.hide); self.b_cancel.pack(side="right")

        self.columnconfigure(1, weight=1)
        self.apply_theme()

    def show(self): self.grid(); self.e_name.focus_set()
    def hide(self): self.grid_remove()

    def apply_theme(self):
        c = self.get_theme()
        set_widget_colors(self, c["panel"], c["fg"])
        for ent in (self.e_name, self.e_reg, self.e_date, self.e_user, self.e_pass):
            ent.configure(bg=c["bg"], fg=c["fg"], insertbackground=c["fg"], highlightbackground=c["border"])
        self.configure(highlightbackground=c["border"])
        for w in self.winfo_children():
            if isinstance(w, tk.Button):
                w.configure(bg=c["btn_bg"], fg=c["btn_fg"], activebackground=c["btn_bg"], activeforeground=c["btn_fg"], highlightbackground=c["border"])

    def do_signup(self):
        name = self.e_name.get().strip()
        reg  = self.e_reg.get().strip()
        dstr = self.e_date.get().strip()

        # Validate incorporation date format
        try:
            inc_date = datetime.fromisoformat(dstr).date()
        except Exception:
            messagebox.showerror("Invalid Date", "Please enter incorporation date in YYYY-MM-DD format.")
            return

        # Validate incorporation date range (must be between 1850 and today)
        today = date.today()
        min_date = date(1850, 1, 1)

        if inc_date > today:
            messagebox.showerror("Invalid Date", "The incorporation date cannot be in the future. Please enter a valid date.")
            return

        if inc_date < min_date:
            messagebox.showerror("Invalid Date", "The incorporation date cannot be before 1850. Please enter a valid date.")
            return

        # Check company age (must be at least 3 years old for MSEG compliance)
        years_since_incorporation = (today - inc_date).days / 365.25
        if years_since_incorporation < 3:
            messagebox.showerror("MSEG Regulatory Compliance Requirement",
                               "The company does not meet the minimum age requirement for MSEG listing. "
                               "Companies must be incorporated for at least 3 years to comply with MSEG regulatory standards.")
            return

        try:
            idx = self.cbo_sector.current()
            sector_id = self.sector_opts[idx][0]
        except Exception:
            sector_id = 1

        user = self.e_user.get().strip()
        pw   = self.e_pass.get().strip()

        if not (name and reg and dstr and user and pw):
            messagebox.showwarning("Missing fields", "All * fields are required.")
            return

        # Validate username (alphanumeric only, max 10 characters)
        if not re.match(r'^[A-Za-z0-9]{1,10}$', user):
            messagebox.showerror("Invalid Username",
                               "Username must contain only letters and numbers, and be no more than 10 characters long.")
            return

        # Validate password (must include uppercase, lowercase, and number; 8-30 characters)
        if len(pw) < 8 or len(pw) > 30:
            messagebox.showerror("Invalid Password",
                               "Password must be between 8 and 30 characters long.")
            return

        if not re.search(r'[A-Z]', pw):
            messagebox.showerror("Invalid Password",
                               "Password must contain at least one uppercase letter.")
            return

        if not re.search(r'[a-z]', pw):
            messagebox.showerror("Invalid Password",
                               "Password must contain at least one lowercase letter.")
            return

        if not re.search(r'[0-9]', pw):
            messagebox.showerror("Invalid Password",
                               "Password must contain at least one number.")
            return

        if username_taken(user):
            messagebox.showerror("Username taken", "Choose a different login username.")
            return

        # Companies House verification
        try:
            self.b_ok.configure(state="disabled"); self.update_idletasks()
            ok, msgs = verify_company_against_ch(name=name, company_no=reg)
        except RuntimeError as e:
            if messagebox.askyesno("Companies House not configured", f"{e}\n\nAdd your API key now?"):
                key = simpledialog.askstring("Companies House API Key", "Enter your API key:", show="*")
                if not key:
                    self.b_ok.configure(state="normal"); return
                try:
                    save_api_key(key)
                    ok, msgs = verify_company_against_ch(name=name, company_no=reg)
                except Exception as ex:
                    self.b_ok.configure(state="normal"); messagebox.showerror("Companies House error", f"{ex}"); return
            else:
                self.b_ok.configure(state="normal"); return
        except Exception as e:
            self.b_ok.configure(state="normal"); messagebox.showerror("Companies House error", f"{e}"); return
        finally:
            self.b_ok.configure(state="normal")

        if not ok:
            messagebox.showerror("Companies House check failed", "\n".join(msgs)); return

        try:
            cid = company_insert(name, reg, dstr, sector_id)
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: company.registration_no" in str(e):
                messagebox.showerror("Duplicate registration", "That registration number already exists.")
            else:
                messagebox.showerror("Database error", str(e))
            return

        add_company_login(user, pw, cid)
        messagebox.showinfo("Success", f"Company created with company_id = {cid}. You can now log in.")
        self.on_success(username=user); self.hide()

# ================= Login =================
class LoginPage(tk.Frame):
    def __init__(self, master, do_login, get_theme):
        super().__init__(master)
        self.do_login = do_login
        self.get_theme = get_theme

        for i in (0,1,2): self.rowconfigure(i, weight=(1 if i!=1 else 0))
        for j in (0,1,2): self.columnconfigure(j, weight=(1 if j!=1 else 0))
        wrapper = tk.Frame(self); wrapper.grid(row=1, column=1)

        self.card = tk.Frame(wrapper, bd=1, relief="solid")
        self.card.grid(row=0, column=0, sticky="nsew")
        self.card.columnconfigure(1, weight=1)

        tk.Label(self.card, text="Login", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16,8))

        tk.Label(self.card, text="Account Type").grid(row=1, column=0, sticky="w", pady=6, padx=(16,6))
        self.role_var = tk.StringVar(value="stock_manager")
        rf = tk.Frame(self.card); rf.grid(row=1, column=1, sticky="w", pady=6, padx=(6,16))
        tk.Radiobutton(rf, text="Stock Manager", variable=self.role_var, value="stock_manager", command=self._role_changed).pack(side="left", padx=(0,12))
        tk.Radiobutton(rf, text="Company", variable=self.role_var, value="company", command=self._role_changed).pack(side="left")

        tk.Label(self.card, text="Username").grid(row=2, column=0, sticky="w", pady=6, padx=(16,6))
        self.e_user = tk.Entry(self.card); self.e_user.grid(row=2, column=1, sticky="ew", pady=6, padx=(6,16))

        tk.Label(self.card, text="Password").grid(row=3, column=0, sticky="w", pady=6, padx=(16,6))
        self.e_pass = tk.Entry(self.card, show="*"); self.e_pass.grid(row=3, column=1, sticky="ew", pady=6, padx=(6,16))

        btn_row = tk.Frame(self.card); btn_row.grid(row=4, column=0, columnspan=2, sticky="e", padx=16, pady=(6,16))
        self.b_login = tk.Button(btn_row, text="Sign In", width=12, command=self._login_clicked); self.b_login.pack(side="right")
        self.b_signup = tk.Button(btn_row, text="Sign Up", width=10, command=self._signup_clicked); self.b_signup.pack_forget()

        self.hint = tk.Label(self.card, text="Demo → Stock Manager: manager1/pass123   |   Company: company1/pass456")
        self.hint.grid(row=5, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 14))

        self.signup_panel = InlineCompanySignup(wrapper, self.get_theme, on_success=self._prefill_after_signup)
        self.signup_panel.grid(row=1, column=0, sticky="ew", pady=(10,0))
        self.signup_panel.grid_remove()

        self.apply_theme()

    def _role_changed(self):
        if self.role_var.get() == "company":
            if not self.b_signup.winfo_ismapped():
                self.b_signup.pack(side="right", padx=(0,8), before=self.b_login)
        else:
            if self.b_signup.winfo_ismapped():
                self.b_signup.pack_forget()
            self.signup_panel.hide()

    def _login_clicked(self):
        role = self.role_var.get().strip()
        user = self.e_user.get().strip()
        pw   = self.e_pass.get().strip()
        if not (role and user and pw):
            messagebox.showwarning("Missing info", "Please select an account type and enter username & password.")
            return
        self.do_login(role, user, pw)

    def _signup_clicked(self):
        if self.signup_panel.winfo_ismapped(): self.signup_panel.hide()
        else: self.signup_panel.show()

    def _prefill_after_signup(self, username):
        self.role_var.set("company"); self._role_changed()
        self.e_user.delete(0, tk.END); self.e_user.insert(0, username)
        self.e_pass.delete(0, tk.END); self.e_pass.focus_set()

    def apply_theme(self):
        c = self.get_theme()
        set_widget_colors(self, c["bg"], c["fg"])
        self.card.configure(bg=c["panel"], highlightbackground=c["border"])
        for ent in (self.e_user, self.e_pass):
            ent.configure(bg=c["bg"], fg=c["fg"], insertbackground=c["fg"], highlightbackground=c["border"])
        self.b_login.configure(bg=c["btn_bg"], fg=c["btn_fg"], activebackground=c["btn_bg"], activeforeground=c["btn_fg"], highlightbackground=c["border"])
        self.b_signup.configure(bg=c["panel"], fg=c["fg"], activebackground=c["panel"], activeforeground=c["fg"], highlightbackground=c["border"])
        self.hint.configure(fg=c["muted"], bg=c["panel"])
        self.signup_panel.apply_theme()

# ================= Company: Application form + list =================
class ApplicationFormPage(tk.Frame):
    def __init__(self, master, get_theme, get_company_id):
        super().__init__(master)
        self.get_theme = get_theme
        self.get_company_id = get_company_id

        self.card = tk.Frame(self, bd=1, relief="solid")
        self.card.pack(fill="both", expand=True, padx=22, pady=22)
        self.card.columnconfigure(0, weight=0)
        self.card.columnconfigure(1, weight=1)
        self.card.rowconfigure(1, weight=1)

        self.topbar = tk.Frame(self.card)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=8, pady=(10,6))
        self.btn_new = tk.Button(self.topbar, text="NEW APPLICATION", width=18, command=self.show_new_form)
        self.btn_new.pack(side="left")

        self.left = tk.Frame(self.card, bd=1, relief="solid", width=260)
        self.left.grid(row=1, column=0, sticky="nsw", padx=(8,6), pady=(6,12))
        self.left.grid_propagate(False)
        tk.Label(self.left, text="APPLICATION LIST", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10,6))
        self.listbox = tk.Listbox(self.left, exportselection=False)
        self.scroll = tk.Scrollbar(self.left, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scroll.set, height=20)
        self.listbox.pack(side="left", fill="both", expand=True, padx=(10,0), pady=(0,10))
        self.scroll.pack(side="right", fill="y", padx=(0,10), pady=(0,10))
        self.listbox.bind("<<ListboxSelect>>", self._on_select_app)

        self.right = tk.Frame(self.card, bd=1, relief="solid")
        self.right.grid(row=1, column=1, sticky="nsew", padx=(6,8), pady=(6,12))

        self.mode = None
        self.current_app_id = None
        self._staged_files = []

        self.apply_theme()

    def load_applications(self):
        self.listbox.delete(0, tk.END)
        cid = self.get_company_id()
        if not cid: return
        rows = applications_for_company(cid)
        if not rows:
            self.listbox.insert(tk.END, "— No applications —")
            self.listbox.configure(state="disabled")
        else:
            self.listbox.configure(state="normal")
            for r in rows:
                label = f"#{r['application_id']} [{r['status'][0].upper()}]"
                self.listbox.insert(tk.END, label)

    def clear_right(self):
        for w in self.right.winfo_children(): w.destroy()

    def show_new_form(self):
        self.mode = "form"; self.current_app_id = None; self.clear_right()
        tk.Label(self.right, text="APPLICATION FORM / STATUS", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16,8))

        r = 1
        tk.Label(self.right, text="Company ID").grid(row=r, column=0, sticky="w", padx=(16,6), pady=6)
        tk.Label(self.right, text=str(self.get_company_id() or "-")).grid(row=r, column=1, sticky="w", padx=(6,16), pady=6); r+=1
        tk.Label(self.right, text="Application Date").grid(row=r, column=0, sticky="w", padx=(16,6), pady=6)
        tk.Label(self.right, text=date.today().isoformat()).grid(row=r, column=1, sticky="w", padx=(6,16), pady=6); r+=1
        tk.Label(self.right, text="Proposed Ticker").grid(row=r, column=0, sticky="w", padx=(16,6), pady=6)
        self.e_ticker = tk.Entry(self.right); self.e_ticker.grid(row=r, column=1, sticky="ew", padx=(6,16), pady=6); r+=1
        tk.Label(self.right, text="Proposed Shares").grid(row=r, column=0, sticky="w", padx=(16,6), pady=6)
        self.e_shares = tk.Entry(self.right); self.e_shares.grid(row=r, column=1, sticky="ew", padx=(6,16), pady=6); r+=1
        tk.Label(self.right, text="Proposed Valuation").grid(row=r, column=0, sticky="w", padx=(16,6), pady=6)
        self.e_val = tk.Entry(self.right); self.e_val.grid(row=r, column=1, sticky="ew", padx=(6,16), pady=6); r+=1

        tk.Label(self.right, text="Attachments").grid(row=r, column=0, sticky="nw", padx=(16,6), pady=(8,4))
        self.attach_list = tk.Listbox(self.right, height=5, selectmode="extended")
        self.attach_list.grid(row=r, column=1, sticky="nsew", padx=(6,16), pady=(6,4))
        r += 1
        abtns = tk.Frame(self.right); abtns.grid(row=r, column=1, sticky="w", padx=(6,16), pady=(0,8))
        tk.Button(abtns, text="Add files…", command=self._pick_files_for_new).pack(side="left")
        tk.Button(abtns, text="Remove selected", command=self._remove_selected_new).pack(side="left", padx=(8,0))
        r += 1

        btns = tk.Frame(self.right); btns.grid(row=r, column=0, columnspan=2, sticky="e", padx=16, pady=(10,16))
        tk.Button(btns, text="Submit Application", width=18, command=self.submit).pack(side="right")

        self.right.columnconfigure(1, weight=1)
        self.apply_theme_right()

    def _pick_files_for_new(self):
        paths = filedialog.askopenfilenames(title="Select files to attach")
        for p in paths:
            if p and p not in self._staged_files:
                self._staged_files.append(p)
                self.attach_list.insert(tk.END, os.path.basename(p))

    def _remove_selected_new(self):
        sel = list(self.attach_list.curselection())[::-1]
        for idx in sel:
            self.attach_list.delete(idx)
            del self._staged_files[idx]

    def show_status(self, application_id: int):
        row = application_get(application_id); self.mode = "status"; self.current_app_id = application_id; self.clear_right()
        tk.Label(self.right, text="APPLICATION FORM / STATUS", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16,8))

        items = [("Application ID", row["application_id"]), ("Company ID", row["company_id"]), ("Application Date", row["application_date"]),
                 ("Proposed Ticker", row["proposed_ticker"]), ("Proposed Shares", row["proposed_shares"]),
                 ("Proposed Valuation", row["proposed_valuation"]), ("Status", row["status"])]
        r = 1
        for label, value in items:
            tk.Label(self.right, text=label).grid(row=r, column=0, sticky="w", padx=(16,6), pady=6)
            tk.Label(self.right, text=str(value)).grid(row=r, column=1, sticky="w", padx=(6,16), pady=6); r += 1

        if row["rejection_note"]:
            tk.Label(self.right, text="Rejection Note").grid(row=r, column=0, sticky="nw", padx=(16,6), pady=6)
            tk.Label(self.right, text=row["rejection_note"], justify="left", wraplength=520).grid(row=r, column=1, sticky="w", padx=(6,16), pady=6); r+=1

        tk.Label(self.right, text="Attachments").grid(row=r, column=0, sticky="nw", padx=(16,6), pady=(8,4))
        files_frame = tk.Frame(self.right); files_frame.grid(row=r, column=1, sticky="nsew", padx=(6,16), pady=(6,8)); r += 1
        files_frame.columnconfigure(0, weight=1)
        self.files_list = tk.Listbox(files_frame, height=6, selectmode="extended")
        self.files_list.grid(row=0, column=0, sticky="nsew")
        sbar = tk.Scrollbar(files_frame, orient="vertical", command=self.files_list.yview)
        sbar.grid(row=0, column=1, sticky="ns")
        self.files_list.configure(yscrollcommand=sbar.set)

        self._frows = attachments_for_application(application_id)
        if not self._frows:
            self.files_list.insert(tk.END, "— No attachments —")
            self.files_list.configure(state="disabled")
        else:
            for a in self._frows:
                self.files_list.insert(tk.END, f"{a['attachment_id']}   {a['filename']}")

        row_btns = tk.Frame(self.right); row_btns.grid(row=r, column=1, sticky="w", padx=(6,16), pady=(0,10)); r += 1
        def _open_selected():
            if self.files_list.cget("state") == "disabled": return
            sel = self.files_list.curselection()
            if not sel: return
            for i in sel:
                apath = attachment_abs_path(self._frows[i]["stored_path"])
                _open_file_with_os(apath)
        tk.Button(row_btns, text="Open", command=_open_selected).pack(side="left")

        if row["status"] == "pending":
            def _add_more():
                paths = filedialog.askopenfilenames(title="Select files to attach")
                for p in paths:
                    try: attachment_store_from_path(application_id, p)
                    except Exception as e:
                        messagebox.showwarning("Attachment skipped", f"{os.path.basename(p)}: {e}")
                self.show_status(application_id)
            tk.Button(row_btns, text="Attach more…", command=_add_more).pack(side="left", padx=(8,0))

        self.right.columnconfigure(1, weight=1)
        self.apply_theme_right()

    def _on_select_app(self, event):
        if self.listbox.cget("state") == "disabled": return
        sel = self.listbox.curselection()
        if not sel: return
        text = self.listbox.get(sel[0])
        m = re.search(r'\d+', text)
        if not m: return
        app_id = int(m.group(0))
        self.show_status(app_id)

    def submit(self):
        cid = self.get_company_id()
        if not cid:
            messagebox.showerror("No company", "Your user is not linked to a company. Please sign in again.")
            return

        # Application date is always today's date (read-only field)
        dstr = date.today().isoformat()

        ticker = self.e_ticker.get().strip().upper()
        shares = self.e_shares.get().strip()
        valuation = self.e_val.get().strip()

        # Check for missing required fields
        if not ticker:
            messagebox.showerror("Missing Field", "Please input Proposed Ticker.")
            return
        if not shares:
            messagebox.showerror("Missing Field", "Please input Proposed Shares.")
            return
        if not valuation:
            messagebox.showerror("Missing Field", "Please input Proposed Valuation.")
            return

        # Check ticker format (3-4 capital letters only)
        if not re.match(r'^[A-Z]{3,4}$', ticker):
            messagebox.showerror("Invalid Format", "Proposed Ticker must be 3 to 4 capital LETTERS only.")
            return

        # Check if ticker already exists in stock market
        with db() as con:
            existing_stock = con.execute("SELECT ticker FROM stock WHERE ticker=?", (ticker,)).fetchone()
            if existing_stock:
                messagebox.showerror("Ticker Already Exists", f"The ticker symbol '{ticker}' is already listed in the stock market. Please choose a different ticker.")
                return

        # Validate shares format (numbers only)
        try:
            shares_i = int(shares)
            if shares_i <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Format", "Proposed Shares must be numbers only (positive integer).")
            return

        # Validate valuation format (numbers only)
        try:
            valuation_i = int(valuation)
            if valuation_i <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Format", "Proposed Valuation must be numbers only (positive integer).")
            return

        # Check for inflated valuation (> 500 billion)
        if valuation_i > 500_000_000_000:
            messagebox.showerror("Inflated Valuation", "The proposed valuation exceeds 500 billion. This valuation appears to be inflated and does not meet MSEG listing requirements.")
            return

        # Check for deflated valuation (< 100 million)
        if valuation_i < 100_000_000:
            messagebox.showerror("Deflated Valuation", "The proposed valuation is below 100 million. This does not meet the minimum MSEG listing requirements.")
            return

        # Check for attachments
        if not self._staged_files:
            messagebox.showerror("Missing Attachments", "Please upload legal, financial, and corporate governance documents.")
            return

        try:
            app_id = application_insert(cid, dstr, ticker, shares_i, valuation_i)
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Database error", str(e))
            return

        saved = 0
        for p in self._staged_files:
            try:
                attachment_store_from_path(app_id, p); saved += 1
            except Exception as e:
                messagebox.showwarning("Attachment skipped", f"{os.path.basename(p)}: {e}")
        self._staged_files = []

        messagebox.showinfo("Submitted", f"Application submitted (ID = {app_id}). Saved {saved} attachment(s).")
        self.load_applications()
        self.show_status(app_id)

    def apply_theme(self):
        c = self.get_theme()
        set_widget_colors(self, c["bg"], c["fg"])
        self.card.configure(bg=c["panel"], highlightbackground=c["border"])
        set_widget_colors(self.topbar, c["panel"], c["fg"])
        self.btn_new.configure(bg=c["panel"], fg=c["fg"], activebackground=c["panel"], activeforeground=c["fg"], highlightbackground=c["border"])
        self.left.configure(bg=c["panel"], highlightbackground=c["border"])
        self.listbox.configure(bg=c["bg"], fg=c["fg"], highlightbackground=c["border"])
        self.right.configure(bg=c["panel"], highlightbackground=c["border"])

    def apply_theme_right(self):
        c = self.get_theme()
        set_widget_colors(self.right, c["panel"], c["fg"])
        for w in self.right.winfo_children():
            if isinstance(w, tk.Button):
                w.configure(bg=c["btn_bg"], fg=c["btn_fg"], activebackground=c["btn_bg"], activeforeground=c["btn_fg"], highlightbackground=c["border"])

    def refresh_company(self):
        self.load_applications(); self.show_new_form()

# Replace the ManagerPortalPage class in your pages.py with this updated version

class ManagerPortalPage(tk.Frame):
    def __init__(self, master, get_theme, refresh_stock_market=None):
        super().__init__(master)
        self.get_theme = get_theme
        self.refresh_stock_market = refresh_stock_market

        self.card = tk.Frame(self, bd=1, relief="solid")
        self.card.pack(fill="both", expand=True, padx=22, pady=22)
        self.card.columnconfigure(0, weight=0)
        self.card.columnconfigure(1, weight=1)
        self.card.rowconfigure(1, weight=1)

        self.topbar = tk.Frame(self.card)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=8, pady=(10,6))
        self.topbar.grid_columnconfigure(0, weight=1)
        
        actions = tk.Frame(self.topbar)
        actions.grid(row=0, column=1, sticky="e")
        self.approve_btn = tk.Button(actions, text="APPROVE", width=12, state="disabled", command=self._approve_current)
        self.approve_btn.pack(side="left")
        self.reject_btn = tk.Button(actions, text="REJECT", width=12, state="disabled", command=self._toggle_reject_panel)
        self.reject_btn.pack(side="left", padx=(8,0))

        self.left = tk.Frame(self.card, bd=1, relief="solid", width=260)
        self.left.grid(row=1, column=0, sticky="nsew", padx=(8,6), pady=(6,12))
        self.left.grid_propagate(False)
        self.left.grid_rowconfigure(0, weight=0)  # Label
        self.left.grid_rowconfigure(1, weight=1)  # Pending list
        self.left.grid_rowconfigure(2, weight=0)  # Label
        self.left.grid_rowconfigure(3, weight=1)  # Approved list
        self.left.grid_rowconfigure(4, weight=0)  # Label
        self.left.grid_rowconfigure(5, weight=1)  # Rejected list
        
        # PENDING APPLICATIONS
        tk.Label(self.left, text="PENDING", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10,4))
        
        pending_frame = tk.Frame(self.left)
        pending_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,8))
        pending_frame.grid_rowconfigure(0, weight=1)
        pending_frame.grid_columnconfigure(0, weight=1)
        
        self.lb_pending = tk.Listbox(pending_frame, exportselection=False)
        scroll_pending = tk.Scrollbar(pending_frame, orient="vertical", command=self.lb_pending.yview)
        self.lb_pending.configure(yscrollcommand=scroll_pending.set)
        self.lb_pending.grid(row=0, column=0, sticky="nsew")
        scroll_pending.grid(row=0, column=1, sticky="ns")
        self.lb_pending.bind("<<ListboxSelect>>", self._on_select_pending)
        
        # APPROVED APPLICATIONS
        tk.Label(self.left, text="APPROVED", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=(8,4))
        
        approved_frame = tk.Frame(self.left)
        approved_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0,8))
        approved_frame.grid_rowconfigure(0, weight=1)
        approved_frame.grid_columnconfigure(0, weight=1)
        
        self.lb_approved = tk.Listbox(approved_frame, exportselection=False)
        scroll_approved = tk.Scrollbar(approved_frame, orient="vertical", command=self.lb_approved.yview)
        self.lb_approved.configure(yscrollcommand=scroll_approved.set)
        self.lb_approved.grid(row=0, column=0, sticky="nsew")
        scroll_approved.grid(row=0, column=1, sticky="ns")
        self.lb_approved.bind("<<ListboxSelect>>", self._on_select_approved)
        
        # REJECTED APPLICATIONS
        tk.Label(self.left, text="REJECTED", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=(8,4))
        
        rejected_frame = tk.Frame(self.left)
        rejected_frame.grid(row=5, column=0, sticky="nsew", padx=10, pady=(0,10))
        rejected_frame.grid_rowconfigure(0, weight=1)
        rejected_frame.grid_columnconfigure(0, weight=1)
        
        self.lb_rejected = tk.Listbox(rejected_frame, exportselection=False)
        scroll_rejected = tk.Scrollbar(rejected_frame, orient="vertical", command=self.lb_rejected.yview)
        self.lb_rejected.configure(yscrollcommand=scroll_rejected.set)
        self.lb_rejected.grid(row=0, column=0, sticky="nsew")
        scroll_rejected.grid(row=0, column=1, sticky="ns")
        self.lb_rejected.bind("<<ListboxSelect>>", self._on_select_rejected)

        self.right = tk.Frame(self.card, bd=1, relief="solid")
        self.right.grid(row=1, column=1, sticky="nsew", padx=(6,8), pady=(6,12))

        self.reject_panel = tk.Frame(self.right)
        self.current_id = None
        self.apply_theme()

    def _approve_current(self):
        """Mark the currently selected application as approved and create stock listing."""
        if not self.current_id:
            messagebox.showwarning("No Selection", "Please select an application first.")
            return
        
        if not messagebox.askyesno("Confirm Approval", "Approve this application and create stock listing?"):
            return
        
        try:
            application_set_approved(self.current_id)
            stock_create_from_application(self.current_id)
            messagebox.showinfo("Approved", "Application approved and stock created successfully.")
        except Exception as e:
            messagebox.showerror("Approve failed", f"Error: {e}")
            return

        if self.refresh_stock_market:
            try:
                self.refresh_stock_market()
            except Exception:
                pass

        self.current_id = None
        self.reject_panel.grid_remove()
        self.load_list()

    def _toggle_reject_panel(self):
        if not self.current_id:
            messagebox.showwarning("No Selection", "Please select an application first.")
            return
        if self.reject_panel.winfo_ismapped():
            self.reject_panel.grid_remove()
        else:
            self._show_reject_panel()

    def _show_reject_panel(self):
        for w in self.reject_panel.winfo_children():
            w.destroy()
        tk.Label(self.reject_panel, text="Rejection Note (required)").grid(row=0, column=0, sticky="w", padx=(16,6), pady=(6,4))
        self.txt = tk.Text(self.reject_panel, height=6, width=60)
        self.txt.grid(row=1, column=0, sticky="ew", padx=(16,16))
        btns = tk.Frame(self.reject_panel)
        btns.grid(row=2, column=0, sticky="e", padx=16, pady=(6,12))
        tk.Button(btns, text="Save Rejection", command=self._save_rejection).pack(side="right")
        tk.Button(btns, text="Cancel", command=lambda: self.reject_panel.grid_remove()).pack(side="right", padx=(0,8))
        self.reject_panel.grid(row=99, column=0, columnspan=2, sticky="ew")
        self.apply_theme()

    def _save_rejection(self):
        note = self.txt.get("1.0", "end").strip()
        if not note:
            messagebox.showwarning("Required", "Please provide a rejection note.")
            return

        full_note = "Stage 2 - Regulatory Compliance Failed\n" + note
        try:
            application_set_rejected(self.current_id, full_note)
            messagebox.showinfo("Saved", "Application marked as rejected.")
        except Exception as e:
            messagebox.showerror("Reject failed", f"Error: {e}")
            return

        self.current_id = None
        self.reject_panel.grid_remove()
        self.load_list()

    def load_list(self):
        print("DEBUG: load_list() called")
        
        # Clear all listboxes
        self.lb_pending.delete(0, tk.END)
        self.lb_approved.delete(0, tk.END)
        self.lb_rejected.delete(0, tk.END)

        # Get all applications
        all_apps = applications_all()
        print(f"DEBUG: Total applications found: {len(all_apps)}")
        
        # Debug: Print all statuses
        for app in all_apps:
            print(f"DEBUG: App #{app['application_id']} has status: '{app['status']}' (type: {type(app['status'])})")
        
        # Separate by status
        pending_apps = [a for a in all_apps if a["status"].lower().strip() == "pending"]
        approved_apps = [a for a in all_apps if a["status"].lower().strip() == "approved"]
        rejected_apps = [a for a in all_apps if a["status"].lower().strip() == "rejected"]
        
        print(f"DEBUG: Pending: {len(pending_apps)}, Approved: {len(approved_apps)}, Rejected: {len(rejected_apps)}")
        
        # Load pending
        if not pending_apps:
            self.lb_pending.insert(tk.END, "— No applications —")
            self.lb_pending.configure(state="disabled")
        else:
            self.lb_pending.configure(state="normal")
            for r in pending_apps:
                self.lb_pending.insert(tk.END, f"#{r['application_id']}")
        
        # Load approved
        if not approved_apps:
            self.lb_approved.insert(tk.END, "— No applications —")
            self.lb_approved.configure(state="disabled")
        else:
            self.lb_approved.configure(state="normal")
            for r in approved_apps:
                self.lb_approved.insert(tk.END, f"#{r['application_id']}")
        
        # Load rejected
        if not rejected_apps:
            self.lb_rejected.insert(tk.END, "— No applications —")
            self.lb_rejected.configure(state="disabled")
        else:
            self.lb_rejected.configure(state="normal")
            for r in rejected_apps:
                self.lb_rejected.insert(tk.END, f"#{r['application_id']}")
        
        # Don't auto-select anything - start with empty details pane
        self.current_id = None
        self.approve_btn.configure(state="disabled")
        self.reject_btn.configure(state="disabled")
        
        # Clear the details pane
        for w in self.right.winfo_children():
            if w is not self.reject_panel:
                w.destroy()
        
        # Show a message prompting user to select an application
        tk.Label(self.right, text="Select an application to view details", 
                font=("Segoe UI", 11), fg="gray").place(relx=0.5, rely=0.5, anchor="center")

    def _on_select_pending(self, event):
        self._clear_other_selections(self.lb_pending)
        if self.lb_pending.cget("state") == "disabled":
            return
        sel = self.lb_pending.curselection()
        if not sel:
            return
        text = self.lb_pending.get(sel[0])
        m = re.search(r'\d+', text)
        if not m:
            return
        app_id = int(m.group(0))
        self.show_details(app_id)

    def _on_select_approved(self, event):
        self._clear_other_selections(self.lb_approved)
        if self.lb_approved.cget("state") == "disabled":
            return
        sel = self.lb_approved.curselection()
        if not sel:
            return
        text = self.lb_approved.get(sel[0])
        m = re.search(r'\d+', text)
        if not m:
            return
        app_id = int(m.group(0))
        self.show_details(app_id)

    def _on_select_rejected(self, event):
        self._clear_other_selections(self.lb_rejected)
        if self.lb_rejected.cget("state") == "disabled":
            return
        sel = self.lb_rejected.curselection()
        if not sel:
            return
        text = self.lb_rejected.get(sel[0])
        m = re.search(r'\d+', text)
        if not m:
            return
        app_id = int(m.group(0))
        self.show_details(app_id)

    def _clear_other_selections(self, active_listbox):
        """Clear selections in other listboxes."""
        for lb in [self.lb_pending, self.lb_approved, self.lb_rejected]:
            if lb != active_listbox and lb.cget("state") != "disabled":
                lb.selection_clear(0, tk.END)

    def show_details(self, app_id):
        row = application_get(app_id)
        if not row:
            return
        
        self.current_id = app_id

        for w in self.right.winfo_children():
            if w is not self.reject_panel:
                w.destroy()

        tk.Label(self.right, text="APPLICATION DETAILS", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 8))

        r = 1
        items = [
            ("Application ID", row["application_id"]),
            ("Company ID", row["company_id"]),
            ("Application Date", row["application_date"]),
            ("Proposed Ticker", row["proposed_ticker"]),
            ("Proposed Shares", row["proposed_shares"]),
            ("Proposed Valuation", row["proposed_valuation"]),
            ("Status", row["status"]),
        ]
        for label, value in items:
            tk.Label(self.right, text=label).grid(row=r, column=0, sticky="w", padx=(16, 6), pady=6)
            tk.Label(self.right, text=str(value)).grid(row=r, column=1, sticky="w", padx=(6, 16), pady=6)
            r += 1

        if row["rejection_note"]:
            tk.Label(self.right, text="Rejection Note").grid(row=r, column=0, sticky="nw", padx=(16, 6), pady=6)
            tk.Label(self.right, text=row["rejection_note"], justify="left", wraplength=520).grid(row=r, column=1, sticky="w", padx=(6, 16), pady=6)
            r += 1

        tk.Label(self.right, text="Attachments").grid(row=r, column=0, sticky="nw", padx=(16, 6), pady=(8, 4))
        mfiles = tk.Frame(self.right)
        mfiles.grid(row=r, column=1, sticky="nsew", padx=(6, 16), pady=(6, 8))
        r += 1

        mfiles.columnconfigure(0, weight=1)
        self.mfiles_list = tk.Listbox(mfiles, height=6, selectmode="extended")
        self.mfiles_list.grid(row=0, column=0, sticky="nsew")
        ms = tk.Scrollbar(mfiles, orient="vertical", command=self.mfiles_list.yview)
        ms.grid(row=0, column=1, sticky="ns")
        self.mfiles_list.configure(yscrollcommand=ms.set)

        self._mrows = attachments_for_application(app_id)
        if not self._mrows:
            self.mfiles_list.insert(tk.END, "— No attachments —")
            self.mfiles_list.configure(state="disabled")
        else:
            for a in self._mrows:
                self.mfiles_list.insert(tk.END, f"{a['attachment_id']}   {a['filename']}")

        mbtns = tk.Frame(self.right)
        mbtns.grid(row=r, column=1, sticky="w", padx=(6, 16), pady=(0, 10))
        r += 1

        def _m_open():
            if self.mfiles_list.cget("state") == "disabled":
                return
            sel = self.mfiles_list.curselection()
            if not sel:
                return
            for i in sel:
                apath = attachment_abs_path(self._mrows[i]["stored_path"])
                _open_file_with_os(apath)

        def _m_download():
            if self.mfiles_list.cget("state") == "disabled":
                return
            sel = self.mfiles_list.curselection()
            if not sel:
                return
            dest_dir = filedialog.askdirectory(title="Choose download folder")
            if not dest_dir:
                return
            for i in sel:
                rowf = self._mrows[i]
                src = attachment_abs_path(rowf["stored_path"])
                try:
                    shutil.copy2(src, os.path.join(dest_dir, rowf["filename"]))
                except Exception as e:
                    messagebox.showwarning("Download error", f"{rowf['filename']}: {e}")
            messagebox.showinfo("Downloaded", "Selected files copied to the chosen folder.")

        tk.Button(mbtns, text="Open", command=_m_open).pack(side="left")
        tk.Button(mbtns, text="Download…", command=_m_download).pack(side="left", padx=(8, 0))

        # Internal notes section
        tk.Label(self.right, text="Internal notes").grid(row=r, column=0, sticky="nw", padx=(16, 6), pady=(8, 4))
        self._notes = tk.Text(self.right, height=4, width=60)
        self._notes.grid(row=r, column=1, sticky="ew", padx=(6, 16), pady=(6, 8))
        r += 1

        if row["internal_notes"]:
            self._notes.insert("1.0", row["internal_notes"])

        nb = tk.Frame(self.right)
        nb.grid(row=r, column=1, sticky="e", padx=(6, 16), pady=(0, 8))
        r += 1

        # Get current status
        status = (row["status"] or "").strip().lower()
        
        # For approved/rejected applications, make notes read-only
        if status in ("approved", "rejected"):
            self._notes.configure(state="disabled")
        else:
            # Only allow saving notes for pending applications
            def _save_notes():
                application_set_internal_notes(app_id, self._notes.get("1.0", "end").strip())
                messagebox.showinfo("Saved", "Internal notes saved.")
            tk.Button(nb, text="Save notes", command=_save_notes).pack(side="right")

        # CRITICAL: Only enable APPROVE/REJECT buttons for pending applications
        if status == "pending":
            self.approve_btn.configure(state="normal")
            self.reject_btn.configure(state="normal")
        else:
            self.approve_btn.configure(state="disabled")
            self.reject_btn.configure(state="disabled")

        self.right.columnconfigure(1, weight=1)
        self.apply_theme()

    def apply_theme(self):
        c = self.get_theme()
        set_widget_colors(self, c["bg"], c["fg"])
        self.card.configure(bg=c["panel"], highlightbackground=c["border"])
        set_widget_colors(self.topbar, c["panel"], c["fg"])
        self.left.configure(bg=c["panel"], highlightbackground=c["border"])
        
        for lb in [self.lb_pending, self.lb_approved, self.lb_rejected]:
            lb.configure(bg=c["bg"], fg=c["fg"], highlightbackground=c["border"])
        
        self.right.configure(bg=c["panel"], highlightbackground=c["border"])
        for frame in self.topbar.winfo_children():
            for w in frame.winfo_children():
                if isinstance(w, tk.Button):
                    w.configure(bg=c["panel"], fg=c["fg"], activebackground=c["panel"], activeforeground=c["fg"], highlightbackground=c["border"])