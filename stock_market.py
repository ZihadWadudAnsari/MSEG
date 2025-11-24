import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from db import stocks_all, stock_delete, stock_calculate_return, stock_calculate_24hr_change, sectors_all, stock_get_prices
from ui_components import set_widget_colors

class StockMarketPage(tk.Frame):
    def __init__(self, master, get_theme, readonly=False):
        super().__init__(master)
        self.get_theme = get_theme
        self.readonly = readonly
        self.selected_stocks = set()
        
        self.card = tk.Frame(self, bd=1, relief="solid")
        self.card.pack(fill="both", expand=True, padx=22, pady=22)
        
        # Top toolbar (only show if not readonly)
        if not self.readonly:
            self.toolbar = tk.Frame(self.card)
            self.toolbar.pack(fill="x", padx=8, pady=(10, 6))
            
            # Left side buttons
            left_btns = tk.Frame(self.toolbar)
            left_btns.pack(side="left")
            
            self.btn_select_all = tk.Button(left_btns, text="SELECT ALL", width=12, command=self.select_all)
            self.btn_select_all.pack(side="left", padx=(0, 8))
            
            self.btn_deselect_all = tk.Button(left_btns, text="DESELECT ALL", width=12, command=self.deselect_all)
            self.btn_deselect_all.pack(side="left", padx=(0, 8))
            
            self.btn_filter = tk.Button(left_btns, text="FILTER", width=12, command=self.show_filter)
            self.btn_filter.pack(side="left", padx=(0, 8))
            
            self.btn_delete = tk.Button(left_btns, text="DELETE", width=12, command=self.delete_selected)
            self.btn_delete.pack(side="left")
            
            # Right side buttons
            right_btns = tk.Frame(self.toolbar)
            right_btns.pack(side="right")
            
            self.btn_analysis = tk.Button(right_btns, text="STOCK ANALYSIS", width=15, command=self.show_analysis_menu)
            self.btn_analysis.pack(side="left", padx=(0, 8))
            
            self.btn_report = tk.Button(right_btns, text="MARKET REPORT", width=15, command=self.generate_market_report)
            self.btn_report.pack(side="left")
        
        # Stock listing table
        self.table_frame = tk.Frame(self.card)
        self.table_frame.pack(fill="both", expand=True, padx=8, pady=(6, 12))
        
        # Create treeview with columns - New order: ticker, price, sector, 24hr, 1m, 6m, 1y
        columns = ("ticker", "price", "sector", "24hr", "1m", "6m", "1y")

        self.tree = ttk.Treeview(self.table_frame, columns=columns, show=("tree headings" if not readonly else "headings"), selectmode="none")

        # Column headers
        if not readonly:
            self.tree.heading("#0", text="☐", anchor="w")
        self.tree.heading("ticker", text="TICKER", anchor="w")
        self.tree.heading("price", text="STOCK PRICE", anchor="e")
        self.tree.heading("sector", text="SECTOR", anchor="w")
        self.tree.heading("24hr", text="24HR", anchor="e")
        self.tree.heading("1m", text="1M", anchor="e")
        self.tree.heading("6m", text="6M", anchor="e")
        self.tree.heading("1y", text="1Y", anchor="e")

        # Column widths
        if not readonly:
            self.tree.column("#0", width=40, stretch=False)
        self.tree.column("ticker", width=100)
        self.tree.column("price", width=120)
        self.tree.column("sector", width=200)
        self.tree.column("24hr", width=90)
        self.tree.column("1m", width=90)
        self.tree.column("6m", width=90)
        self.tree.column("1y", width=90)
        
        # Scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Bind click event on checkbox column (only if not readonly)
        if not readonly:
            self.tree.bind("<Button-1>", self.on_tree_click)
        
        self.current_filter_sectors = None
        self.load_stocks()
        self.apply_theme()
    
    def on_tree_click(self, event):
        """Handle clicks on the tree, particularly on the checkbox column."""
        region = self.tree.identify_region(event.x, event.y)
        if region == "tree":
            item = self.tree.identify_row(event.y)
            if item:
                self.toggle_selection(item)
    
    def toggle_selection(self, item):
        """Toggle selection state of an item."""
        stock_id = int(item.split("_")[1]) if "_" in item else None
        if not stock_id:
            return
        
        if stock_id in self.selected_stocks:
            self.selected_stocks.remove(stock_id)
            self.tree.item(item, text="☐")
        else:
            self.selected_stocks.add(stock_id)
            self.tree.item(item, text="☑")
    
    def select_all(self):
        """Select all stocks."""
        for item in self.tree.get_children():
            stock_id = int(item.split("_")[1]) if "_" in item else None
            if stock_id:
                self.selected_stocks.add(stock_id)
                self.tree.item(item, text="☑")
    
    def deselect_all(self):
        """Deselect all stocks."""
        self.selected_stocks.clear()
        for item in self.tree.get_children():
            self.tree.item(item, text="☐")
    
    def show_filter(self):
        """Show sector filter dialog."""
        dialog = tk.Toplevel(self)
        dialog.title("Filter by Sector")
        dialog.geometry("400x500")
        dialog.transient(self)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select Sectors to Display:", font=("Segoe UI", 11, "bold")).pack(pady=(10, 5), padx=10, anchor="w")
        
        # Sector checkboxes
        frame = tk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        sector_vars = {}
        sectors = sectors_all()
        for sector in sectors:
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(frame, text=sector["sector_name"], variable=var)
            cb.pack(anchor="w", pady=2)
            sector_vars[sector["sector_id"]] = var
        
        # Buttons
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def apply_filter():
            selected = [sid for sid, var in sector_vars.items() if var.get()]
            if not selected:
                messagebox.showwarning("No Selection", "Please select at least one sector.")
                return
            self.current_filter_sectors = selected
            self.load_stocks()
            dialog.destroy()
        
        def clear_filter():
            self.current_filter_sectors = None
            self.load_stocks()
            dialog.destroy()
        
        tk.Button(btn_frame, text="Apply Filter", command=apply_filter, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear Filter", command=clear_filter, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy, width=12).pack(side="left", padx=5)
    
    def delete_selected(self):
        """Delete selected stocks."""
        if not self.selected_stocks:
            messagebox.showwarning("No Selection", "Please select at least one stock to delete.")
            return
        
        if not messagebox.askyesno("Confirm Delete", f"Delete {len(self.selected_stocks)} selected stock(s)?"):
            return
        
        for stock_id in self.selected_stocks:
            try:
                stock_delete(stock_id)
            except Exception as e:
                messagebox.showerror("Delete Error", f"Failed to delete stock {stock_id}: {e}")
        
        self.selected_stocks.clear()
        self.load_stocks()
        messagebox.showinfo("Success", "Selected stocks deleted.")
    
    def show_analysis_menu(self):
        """Show analysis options menu."""
        if not self.selected_stocks:
            messagebox.showwarning("No Selection", "Please select at least one stock for analysis.")
            return
        
        dialog = tk.Toplevel(self)
        dialog.title("Stock Analysis Options")
        dialog.geometry("450x300")
        dialog.transient(self)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select Analysis Type:", font=("Segoe UI", 12, "bold")).pack(pady=(15, 10))
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(expand=True)
        
        tk.Button(btn_frame, text="1. Time-framed Returns", width=30, 
                 command=lambda: [dialog.destroy(), self.analysis_timeframed_returns()]).pack(pady=8)
        tk.Button(btn_frame, text="2. Valuation Comparison", width=30,
                 command=lambda: [dialog.destroy(), self.analysis_valuation_comparison()]).pack(pady=8)
        tk.Button(btn_frame, text="3. Sector Benchmarking", width=30,
                 command=lambda: [dialog.destroy(), self.analysis_sector_benchmarking()]).pack(pady=8)
        tk.Button(btn_frame, text="4. Performance Consistency Score", width=30,
                 command=lambda: [dialog.destroy(), self.analysis_performance_consistency()]).pack(pady=8)
        
        tk.Button(dialog, text="Cancel", command=dialog.destroy, width=12).pack(pady=(10, 15))
    
    def analysis_timeframed_returns(self):
        """Generate time-framed returns analysis."""
        stocks = stocks_all()
        stock_dict = {s["stock_id"]: s for s in stocks}

        lines = ["TIME-FRAMED RETURNS ANALYSIS", "=" * 60, ""]
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Selected Stocks: {len(self.selected_stocks)}")
        lines.append("")
        lines.append(f"{'Ticker':<12} {'1 Month':<12} {'6 Months':<12} {'1 Year':<12}")
        lines.append("-" * 60)

        for stock_id in sorted(self.selected_stocks):
            if stock_id in stock_dict:
                stock = stock_dict[stock_id]
                r1m = stock_calculate_return(stock_id, 30)
                r6m = stock_calculate_return(stock_id, 180)
                r1y = stock_calculate_return(stock_id, 365)

                lines.append(f"{stock['ticker']:<12} {r1m:>10.2f}% {r6m:>10.2f}% {r1y:>10.2f}%")

        self.show_report_window("Time-Framed Returns Analysis", "\n".join(lines), "timeframed_returns.txt")
    
    def analysis_valuation_comparison(self):
        """Generate valuation comparison analysis."""
        stocks = stocks_all()
        stock_dict = {s["stock_id"]: s for s in stocks}

        lines = ["VALUATION COMPARISON ANALYSIS", "=" * 80, ""]
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Selected Stocks: {len(self.selected_stocks)}")
        lines.append("")
        lines.append(f"{'Ticker':<12} {'Current Price':<15} {'Valuation':<15} {'Shares':<15} {'1Y Growth':<12}")
        lines.append("-" * 80)

        for stock_id in sorted(self.selected_stocks):
            if stock_id in stock_dict:
                stock = stock_dict[stock_id]
                current_val = stock["current_price"] * stock["shares_outstanding"] if stock["current_price"] else 0
                growth = stock_calculate_return(stock_id, 365)

                lines.append(f"{stock['ticker']:<12} ${stock['current_price']:>13,.2f} "
                           f"${current_val:>13,.0f} {stock['shares_outstanding']:>14,} {growth:>10.2f}%")

        self.show_report_window("Valuation Comparison Analysis", "\n".join(lines), "valuation_comparison.txt")
    
    def analysis_sector_benchmarking(self):
        """Generate sector benchmarking analysis."""
        stocks = stocks_all()
        stock_dict = {s["stock_id"]: s for s in stocks}

        # Calculate sector averages
        sector_returns = {}

        for stock in stocks:
            if stock["sector_id"]:
                r1y = stock_calculate_return(stock["stock_id"], 365)
                if stock["sector_id"] not in sector_returns:
                    sector_returns[stock["sector_id"]] = []
                sector_returns[stock["sector_id"]].append(r1y)

        sector_avgs = {sid: sum(rets)/len(rets) if rets else 0
                      for sid, rets in sector_returns.items()}

        lines = ["SECTOR BENCHMARKING ANALYSIS", "=" * 80, ""]
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Selected Stocks: {len(self.selected_stocks)}")
        lines.append("")
        lines.append(f"{'Ticker':<12} {'Sector':<25} {'Stock 1Y Return':<18} {'Sector Avg':<15} {'Diff':<10}")
        lines.append("-" * 80)

        for stock_id in sorted(self.selected_stocks):
            if stock_id in stock_dict:
                stock = stock_dict[stock_id]
                r1y = stock_calculate_return(stock_id, 365)
                sector_avg = sector_avgs.get(stock["sector_id"], 0)
                diff = r1y - sector_avg

                lines.append(f"{stock['ticker']:<12} {stock['sector_name']:<25} "
                           f"{r1y:>16.2f}% {sector_avg:>13.2f}% {diff:>+8.2f}%")

        self.show_report_window("Sector Benchmarking Analysis", "\n".join(lines), "sector_benchmarking.txt")
    
    def analysis_performance_consistency(self):
        """Generate performance consistency score analysis."""
        stocks = stocks_all()
        stock_dict = {s["stock_id"]: s for s in stocks}

        lines = ["PERFORMANCE CONSISTENCY SCORE ANALYSIS", "=" * 70, ""]
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Selected Stocks: {len(self.selected_stocks)}")
        lines.append("")
        lines.append("Consistency Score: Lower variance = more consistent performance")
        lines.append("")
        lines.append(f"{'Ticker':<12} {'1M':<10} {'6M':<10} {'1Y':<10} {'Variance':<12} {'Score':<10}")
        lines.append("-" * 70)

        for stock_id in sorted(self.selected_stocks):
            if stock_id in stock_dict:
                stock = stock_dict[stock_id]
                r1m = stock_calculate_return(stock_id, 30)
                r6m = stock_calculate_return(stock_id, 180)
                r1y = stock_calculate_return(stock_id, 365)

                returns = [r1m, r6m, r1y]
                avg = sum(returns) / len(returns)
                variance = sum((r - avg) ** 2 for r in returns) / len(returns)

                # Score: 100 - normalized variance (higher = more consistent)
                score = max(0, 100 - variance)

                lines.append(f"{stock['ticker']:<12} {r1m:>8.2f}% {r6m:>8.2f}% "
                           f"{r1y:>8.2f}% {variance:>10.2f} {score:>8.1f}")

        self.show_report_window("Performance Consistency Analysis", "\n".join(lines), "performance_consistency.txt")
    
    def generate_market_report(self):
        """Generate overall market report."""
        stocks = stocks_all()

        if not stocks:
            messagebox.showinfo("No Data", "No stocks are currently listed.")
            return

        total_companies = len(stocks)
        total_valuation = sum((s["current_price"] or 0) * s["shares_outstanding"] for s in stocks)
        avg_valuation = total_valuation / total_companies if total_companies > 0 else 0

        # Sector distribution
        sector_vals = {}
        for stock in stocks:
            sector_name = stock["sector_name"] or "Unknown"
            stock_val = (stock["current_price"] or 0) * stock["shares_outstanding"]
            sector_vals[sector_name] = sector_vals.get(sector_name, 0) + stock_val

        lines = ["MARKET REPORT", "=" * 60, ""]
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("OVERVIEW")
        lines.append("-" * 60)
        lines.append(f"Total Listed Companies: {total_companies}")
        lines.append(f"Total Market Valuation: ${total_valuation:,.2f}")
        lines.append(f"Average Stock Valuation: ${avg_valuation:,.2f}")
        lines.append("")
        lines.append("SECTOR-WISE VALUATION DISTRIBUTION")
        lines.append("-" * 60)
        lines.append(f"{'Sector':<30} {'Valuation':<20} {'Percentage':<10}")
        lines.append("-" * 60)

        for sector_name, val in sorted(sector_vals.items(), key=lambda x: x[1], reverse=True):
            pct = (val / total_valuation * 100) if total_valuation > 0 else 0
            lines.append(f"{sector_name:<30} ${val:>18,.2f} {pct:>8.1f}%")

        self.show_report_window("Market Report", "\n".join(lines), "market_report.txt")

    def show_report_window(self, title, content, default_filename):
        """Display report in a new window with save button."""
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("900x600")
        window.transient(self)

        # Create frame for content
        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Text widget with scrollbar
        text_frame = tk.Frame(frame)
        text_frame.pack(fill="both", expand=True)

        text_widget = tk.Text(text_frame, wrap="none", font=("Courier New", 10))
        vsb = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        hsb = tk.Scrollbar(text_frame, orient="horizontal", command=text_widget.xview)
        text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        text_widget.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Insert content
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled")  # Make read-only

        # Button frame
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", pady=(10, 0))

        def save_current_report():
            self.save_report_from_window(default_filename, content, window)

        tk.Button(btn_frame, text="Save as TXT", width=15, command=save_current_report).pack(side="right", padx=5)
        tk.Button(btn_frame, text="Close", width=10, command=window.destroy).pack(side="right")

        # Apply theme
        c = self.get_theme()
        window.configure(bg=c["bg"])
        frame.configure(bg=c["bg"])
        text_frame.configure(bg=c["bg"])
        text_widget.configure(bg=c["bg"], fg=c["fg"], insertbackground=c["fg"])
        btn_frame.configure(bg=c["bg"])

    def save_report_from_window(self, default_name, content, parent_window):
        """Save report to file from window."""
        filepath = filedialog.asksaveasfilename(
            parent=parent_window,
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Report saved to:\n{filepath}", parent=parent_window)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {e}", parent=parent_window)

    def save_report(self, default_name, content):
        """Save report to file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Report saved to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {e}")
    
    def load_stocks(self):
        """Load and display all stocks."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        stocks = stocks_all()
        
        # Apply sector filter if active
        if self.current_filter_sectors:
            stocks = [s for s in stocks if s["sector_id"] in self.current_filter_sectors]
        
        if not stocks:
            # Show empty message
            if self.readonly:
                self.tree.insert("", "end", values=("No stocks listed", "", "", "", "", "", ""))
            else:
                self.tree.insert("", "end", text="", values=("No stocks listed", "", "", "", "", "", ""))
            return

        for stock in stocks:
            # Calculate returns - removed 3m, new order: ticker, price, sector, 24hr, 1m, 6m, 1y
            r24hr = stock_calculate_24hr_change(stock["stock_id"])
            r1m = stock_calculate_return(stock["stock_id"], 30)
            r6m = stock_calculate_return(stock["stock_id"], 180)
            r1y = stock_calculate_return(stock["stock_id"], 365)

            # Format values
            price_str = f"${stock['current_price']:,.2f}" if stock['current_price'] else "N/A"
            r24hr_str = f"{r24hr:+.2f}%" if r24hr != 0 else "0.00%"
            r1m_str = f"{r1m:+.2f}%" if r1m != 0 else "0.00%"
            r6m_str = f"{r6m:+.2f}%" if r6m != 0 else "0.00%"
            r1y_str = f"{r1y:+.2f}%" if r1y != 0 else "0.00%"

            if self.readonly:
                # Read-only version (no checkboxes) - New order: ticker, price, sector, 24hr, 1m, 6m, 1y
                self.tree.insert("", "end",
                               values=(stock["ticker"], price_str, stock["sector_name"] or "N/A", r24hr_str,
                                      r1m_str, r6m_str, r1y_str))
            else:
                # Manager version (with checkboxes) - New order: ticker, price, sector, 24hr, 1m, 6m, 1y
                checkbox = "☑" if stock["stock_id"] in self.selected_stocks else "☐"
                item_id = f"stock_{stock['stock_id']}"
                self.tree.insert("", "end", iid=item_id, text=checkbox,
                               values=(stock["ticker"], price_str, stock["sector_name"] or "N/A", r24hr_str,
                                      r1m_str, r6m_str, r1y_str))
    
    def apply_theme(self):
        """Apply current theme to all widgets."""
        c = self.get_theme()
        set_widget_colors(self, c["bg"], c["fg"])
        self.card.configure(bg=c["panel"], highlightbackground=c["border"])
        
        if not self.readonly:
            set_widget_colors(self.toolbar, c["panel"], c["fg"])
            for btn in (self.btn_select_all, self.btn_deselect_all, self.btn_filter, 
                       self.btn_delete, self.btn_analysis, self.btn_report):
                btn.configure(bg=c["panel"], fg=c["fg"], activebackground=c["panel"], 
                             activeforeground=c["fg"], highlightbackground=c["border"])
        
        set_widget_colors(self.table_frame, c["panel"], c["fg"])
    
    def refresh(self):
        """Refresh the stock listing."""
        self.load_stocks()