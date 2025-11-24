import tkinter as tk
from tkinter import messagebox

APP_TITLE = "Manchester Stock Exchange"

from ui_components import Header, THEMES
from pages import LoginPage, ApplicationFormPage, ManagerPortalPage
from stock_market import StockMarketPage
from db import ensure_db
from auth import ensure_users_file, verify_credentials

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1280x960")
        self.minsize(1280, 720)
        self.theme = "light"
        self.user = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = Header(self, on_toggle_theme=self.toggle_theme, on_sign_out=self.sign_out, get_theme=self.theme_colors)
        self.header.grid(row=0, column=0, sticky="ew")

        self.content = tk.Frame(self); self.content.grid(row=1, column=0, sticky="nsew")

        self.pages = {}
        self.pages["login"] = LoginPage(self.content, do_login=self.try_login, get_theme=self.theme_colors)
        self.pages["company"] = ApplicationFormPage(self.content, get_theme=self.theme_colors, get_company_id=self.get_company_id)
        self.pages["manager"] = ManagerPortalPage(self.content, get_theme=self.theme_colors, refresh_stock_market=self.refresh_stock_market)
        self.pages["stock_market"] = StockMarketPage(self.content, get_theme=self.theme_colors)
        self.pages["stock_market_readonly"] = StockMarketPage(self.content, get_theme=self.theme_colors, readonly=True)

        for p in self.pages.values(): p.grid(row=0, column=0, sticky="nsew")
        self.show_page("login")
        self.apply_theme()

    def theme_colors(self): return THEMES[self.theme]
    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()
    def apply_theme(self):
        c = self.theme_colors()
        self.configure(bg=c["bg"])
        self.content.configure(bg=c["bg"])
        self.header.apply_theme()
        for p in self.pages.values():
            if hasattr(p, "apply_theme"): p.apply_theme()
        self.header.dark_btn.configure(text=("Light Mode" if self.theme == "dark" else "Dark Mode"))

    def show_page(self, name):
        self.pages[name].tkraise()
        if name == "login":
            self.header.enable_signout(False)
            self.header.set_nav_text("")
            self.header.hide_nav_buttons()
        else:
            self.header.enable_signout(True)
            self.header.set_nav_text("")  # Remove "NAVIGATION MENU" text
            
            if self.user and self.user.get("role") == "stock_manager":
                self.header.show_nav_buttons(
                    btn1_text="Applications",
                    btn1_command=lambda: self.show_page("manager"),
                    btn2_text="Stock Market",
                    btn2_command=lambda: self.show_page("stock_market")
                )
                self.header.highlight_nav_button(name)
            elif self.user and self.user.get("role") == "company":
                self.header.show_nav_buttons(
                    btn1_text="Applications",
                    btn1_command=lambda: self.show_page("company"),
                    btn2_text="Stock Market",
                    btn2_command=lambda: self.show_page("stock_market_readonly")
                )
                self.header.highlight_nav_button(name if name != "stock_market_readonly" else "stock_market_readonly")
            else:
                self.header.hide_nav_buttons()
            
            if name == "company":
                self.pages["company"].refresh_company()
            elif name == "manager":
                self.pages["manager"].load_list()
            elif name == "stock_market":
                self.pages["stock_market"].refresh()
            elif name == "stock_market_readonly":
                self.pages["stock_market_readonly"].refresh()

    def refresh_stock_market(self):
        """Refresh stock market page after approval."""
        if "stock_market" in self.pages:
            self.pages["stock_market"].refresh()

    def get_company_id(self):
        return self.user.get("company_id") if self.user else None

    def try_login(self, role, username, password):
        info = verify_credentials(role, username, password)
        if not info:
            messagebox.showerror("Login failed", "Invalid credentials.")
            return
        self.user = info
        if info["role"] == "company":
            if not info["company_id"]:
                messagebox.showerror("No company linked",
                                     "This login is not linked to a company record. Please sign up first.")
                self.sign_out(); return
            self.show_page("company")
        else:
            self.show_page("manager")

    def sign_out(self):
        self.user = None
        self.show_page("login")

if __name__ == "__main__":
    ensure_db()
    ensure_users_file()
    app = App()
    app.mainloop()