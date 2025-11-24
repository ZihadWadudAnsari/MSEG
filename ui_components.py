import tkinter as tk
import os

THEMES = {
    "light": {"bg":"#d9d9d9","fg":"#111827","panel":"#f3f4f6","border":"#cbd5e1","btn_bg":"#111827","btn_fg":"#ffffff","muted":"#6b7280","active":"#3b82f6"},
    "dark":  {"bg":"#1b263d","fg":"#e5e7eb","panel":"#0f172a","border":"#334155","btn_bg":"#e5e7eb","btn_fg":"#0b1220","muted":"#93a3b3","active":"#60a5fa"},
}

def set_widget_colors(widget, bg, fg):
    try: widget.configure(bg=bg, fg=fg)
    except tk.TclError:
        try: widget.configure(bg=bg)
        except tk.TclError: pass
    for child in widget.winfo_children():
        set_widget_colors(child, bg, fg)

def style_button(btn, bg, fg, border):
    btn.configure(bg=bg, fg=fg, activebackground=bg, activeforeground=fg, highlightbackground=border)

class Header(tk.Frame):
    def __init__(self, master, on_toggle_theme, on_sign_out, get_theme):
        super().__init__(master)
        self.on_toggle_theme = on_toggle_theme
        self.on_sign_out = on_sign_out
        self.get_theme = get_theme

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
        LOGO_PATH = os.path.join(ASSETS_DIR, "mseg.png")
        self.logo = tk.Label(self, width=72, height=72, relief="solid", bd=1, font=("Segoe UI", 10, "bold"))
        try:
            if os.path.exists(LOGO_PATH):
                self._logo_img = tk.PhotoImage(file=LOGO_PATH).subsample(1, 1)
                self.logo.configure(image=self._logo_img, text="")
            else:
                self.logo.configure(text="LOGO")
        except Exception:
            self.logo.configure(text="LOGO")
        self.logo.grid(row=0, column=0, padx=(14, 10), pady=8, sticky="w")

        # Navigation frame with buttons (smaller and consistent)
        self.nav_frame = tk.Frame(self, relief="solid", bd=1)
        self.nav_frame.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

        self.nav_label = tk.Label(self.nav_frame, text="", font=("Segoe UI", 9, "bold"))
        self.nav_label.pack(side="top", pady=(4, 2))

        # Navigation buttons container
        self.nav_buttons_frame = tk.Frame(self.nav_frame)
        self.nav_buttons_frame.pack(side="top", pady=(0, 4))
        
        self.btn_applications = tk.Button(self.nav_buttons_frame, text="Applications", width=15, state="disabled")
        self.btn_stock_market = tk.Button(self.nav_buttons_frame, text="Stock Market", width=15, state="disabled")

        self.actions = tk.Frame(self)
        self.actions.grid(row=0, column=2, padx=(10, 14), pady=8, sticky="e")

        self.dark_btn = tk.Button(self.actions, text="Dark Mode", width=12, command=self.on_toggle_theme)
        self.dark_btn.grid(row=0, column=0, padx=(0, 8))

        self.signout_btn = tk.Button(self.actions, text="Sign Out", width=10, command=self.on_sign_out, state="disabled")
        self.signout_btn.grid(row=0, column=1)

        self.apply_theme()

    def enable_signout(self, enable=True): 
        self.signout_btn.configure(state=("normal" if enable else "disabled"))
    
    def set_nav_text(self, text): 
        self.nav_label.configure(text=text)
    
    def show_nav_buttons(self, btn1_text, btn1_command, btn2_text, btn2_command):
        """Show navigation buttons."""
        self.btn_applications.configure(text=btn1_text, command=btn1_command, state="normal")
        self.btn_stock_market.configure(text=btn2_text, command=btn2_command, state="normal")
        
        self.btn_applications.pack(side="left", padx=4)
        self.btn_stock_market.pack(side="left", padx=4)
    
    def hide_nav_buttons(self):
        """Hide navigation buttons."""
        self.btn_applications.pack_forget()
        self.btn_stock_market.pack_forget()
    
    def highlight_nav_button(self, page_name):
        """Highlight the active navigation button."""
        c = self.get_theme()
        
        if page_name == "manager" or page_name == "company":
            self.btn_applications.configure(bg=c["active"], fg=c["btn_fg"])
            self.btn_stock_market.configure(bg=c["panel"], fg=c["fg"])
        elif page_name == "stock_market" or page_name == "stock_market_readonly":
            self.btn_stock_market.configure(bg=c["active"], fg=c["btn_fg"])
            self.btn_applications.configure(bg=c["panel"], fg=c["fg"])
        else:
            self.btn_applications.configure(bg=c["panel"], fg=c["fg"])
            self.btn_stock_market.configure(bg=c["panel"], fg=c["fg"])

    def apply_theme(self):
        c = self.get_theme()
        self.configure(bg=c["bg"], highlightbackground=c["border"], highlightthickness=1)
        self.logo.configure(bg=c["panel"], fg=c["fg"], highlightbackground=c["border"])
        self.nav_frame.configure(bg=c["panel"], highlightbackground=c["border"])
        self.nav_label.configure(bg=c["panel"], fg=c["fg"])
        self.nav_buttons_frame.configure(bg=c["panel"])
        self.actions.configure(bg=c["bg"])
        self.dark_btn.configure(bg=c["panel"], fg=c["fg"], activebackground=c["panel"], activeforeground=c["fg"], highlightbackground=c["border"])
        self.signout_btn.configure(bg=c["panel"], fg=c["fg"], activebackground=c["panel"], activeforeground=c["fg"], highlightbackground=c["border"])
        
        # Apply theme to nav buttons
        self.btn_applications.configure(activebackground=c["active"], activeforeground=c["btn_fg"], highlightbackground=c["border"])
        self.btn_stock_market.configure(activebackground=c["active"], activeforeground=c["btn_fg"], highlightbackground=c["border"])