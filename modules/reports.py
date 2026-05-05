"""
Reports screen: low stock, category breakdown, and transaction charts.
Uses matplotlib embedded in tkinter.
"""

import tkinter as tk
from database import get_connection
from theme import COLORS, FONTS
from widgets import CardFrame, StyledButton, DataTable

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class ReportsScreen(tk.Frame):
    """Reports with low stock alerts, charts, and summaries."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self.current_view = "lowstock"
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["bg_main"])
        header.pack(fill="x", padx=24, pady=(20, 10))

        tk.Label(header, text="Reports", font=FONTS["heading_xl"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_main"]).pack(
            side="left")

        # Tab buttons
        tabs = tk.Frame(self, bg=COLORS["bg_main"])
        tabs.pack(fill="x", padx=24, pady=(0, 10))

        self.tab_buttons = {}
        tab_items = [
            ("lowstock", "⚠️ Low Stock"),
            ("category", "📊 By Category"),
            ("supplier", "🏭 By Supplier"),
            ("activity", "📈 Activity"),
        ]

        for key, label in tab_items:
            btn = StyledButton(tabs, text=label,
                               command=lambda k=key: self._switch_tab(k),
                               width=130, height=32,
                               bg=COLORS["primary"] if key == "lowstock"
                               else "#94A3B8")
            btn.pack(side="left", padx=(0, 8))
            self.tab_buttons[key] = btn

        # Content area
        self.content = tk.Frame(self, bg=COLORS["bg_main"])
        self.content.pack(fill="both", expand=True, padx=24, pady=(0, 16))

    def _switch_tab(self, tab_key):
        self.current_view = tab_key
        self._render_content()

    def _render_content(self):
        for w in self.content.winfo_children():
            w.destroy()

        if self.current_view == "lowstock":
            self._render_lowstock()
        elif self.current_view == "category":
            self._render_category_chart()
        elif self.current_view == "supplier":
            self._render_supplier_report()
        elif self.current_view == "activity":
            self._render_activity_chart()

    def _render_lowstock(self):
        """Show products below reorder level."""
        card = CardFrame(self.content)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Products Below Reorder Level",
                 font=FONTS["heading_md"], fg=COLORS["danger"],
                 bg=COLORS["bg_card"]).pack(anchor="w", padx=16, pady=(14, 8))

        columns = ("Name", "SKU", "Current Qty", "Reorder Level",
                   "Shortage", "Location")
        widths = (160, 90, 90, 90, 80, 100)

        table = DataTable(card, columns=columns, column_widths=widths)
        table.pack(fill="both", expand=True, padx=2, pady=2)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT name, sku, quantity, reorder_level, location
            FROM products
            WHERE quantity <= reorder_level
            ORDER BY (reorder_level - quantity) DESC
        """)
        rows = cur.fetchall()
        conn.close()

        data = [(r["name"], r["sku"], r["quantity"], r["reorder_level"],
                 r["reorder_level"] - r["quantity"],
                 r["location"] or "-") for r in rows]
        table.load_data(data)

    def _render_category_chart(self):
        """Pie chart of products by category."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT COALESCE(c.name, 'Uncategorized') as cat, COUNT(p.id) as cnt
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            GROUP BY c.name
            ORDER BY cnt DESC
        """)
        rows = cur.fetchall()
        conn.close()

        if not rows:
            tk.Label(self.content, text="No data available.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_main"]).pack(pady=40)
            return

        labels = [r["cat"] for r in rows]
        values = [r["cnt"] for r in rows]

        if not HAS_MATPLOTLIB:
            self._render_text_report("Products by Category",
                                      labels, values)
            return

        card = CardFrame(self.content)
        card.pack(fill="both", expand=True)

        fig = Figure(figsize=(6, 4), dpi=100, facecolor=COLORS["bg_card"])
        ax = fig.add_subplot(111)

        colors = ["#7C3AED", "#0D9488", "#EA580C", "#2563EB",
                  "#DB2777", "#CA8A04", "#059669", "#DC2626"]
        ax.pie(values, labels=labels, autopct='%1.1f%%',
               colors=colors[:len(values)], startangle=90,
               textprops={'fontsize': 10})
        ax.set_title("Products by Category", fontsize=14, fontweight="bold",
                     pad=16)

        canvas = FigureCanvasTkAgg(fig, card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def _render_supplier_report(self):
        """Products count by supplier."""
        card = CardFrame(self.content)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Products by Supplier",
                 font=FONTS["heading_md"], fg=COLORS["text_primary"],
                 bg=COLORS["bg_card"]).pack(anchor="w", padx=16, pady=(14, 8))

        columns = ("Supplier", "Products", "Total Stock Value")
        widths = (200, 100, 150)

        table = DataTable(card, columns=columns, column_widths=widths)
        table.pack(fill="both", expand=True, padx=2, pady=2)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT COALESCE(s.name, 'No Supplier') as supplier,
                   COUNT(p.id) as cnt,
                   COALESCE(SUM(p.price * p.quantity), 0) as total_value
            FROM products p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            GROUP BY s.name
            ORDER BY total_value DESC
        """)
        rows = cur.fetchall()
        conn.close()

        data = [(r["supplier"], r["cnt"],
                 f"${r['total_value']:,.2f}") for r in rows]
        table.load_data(data)

    def _render_activity_chart(self):
        """Bar chart of recent transaction activity."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DATE(created_at) as date, type,
                   SUM(quantity) as total
            FROM transactions
            GROUP BY DATE(created_at), type
            ORDER BY date DESC
            LIMIT 20
        """)
        rows = cur.fetchall()
        conn.close()

        if not rows:
            tk.Label(self.content, text="No transactions yet.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_main"]).pack(pady=40)
            return

        # Aggregate by date
        dates = {}
        for r in rows:
            d = r["date"]
            if d not in dates:
                dates[d] = {"in": 0, "out": 0}
            dates[d][r["type"]] += r["total"]

        if not HAS_MATPLOTLIB:
            labels = list(dates.keys())
            values = [dates[d]["in"] + dates[d]["out"] for d in labels]
            self._render_text_report("Transaction Activity", labels, values)
            return

        card = CardFrame(self.content)
        card.pack(fill="both", expand=True)

        fig = Figure(figsize=(7, 4), dpi=100, facecolor=COLORS["bg_card"])
        ax = fig.add_subplot(111)

        sorted_dates = sorted(dates.keys())
        in_vals = [dates[d]["in"] for d in sorted_dates]
        out_vals = [dates[d]["out"] for d in sorted_dates]

        x = range(len(sorted_dates))
        bar_w = 0.35

        ax.bar([i - bar_w / 2 for i in x], in_vals, bar_w,
               label="Stock In", color="#16A34A")
        ax.bar([i + bar_w / 2 for i in x], out_vals, bar_w,
               label="Stock Out", color="#DC2626")

        ax.set_xticks(list(x))
        ax.set_xticklabels([d[-5:] for d in sorted_dates], rotation=45,
                            fontsize=9)
        ax.set_title("Transaction Activity", fontsize=14, fontweight="bold")
        ax.legend()
        ax.set_ylabel("Units")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def _render_text_report(self, title, labels, values):
        """Fallback text-based report when matplotlib is not available."""
        card = CardFrame(self.content)
        card.pack(fill="both", expand=True)

        tk.Label(card, text=title, font=FONTS["heading_md"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(
            anchor="w", padx=16, pady=(14, 8))

        tk.Label(card, text="(Install matplotlib for charts: pip install matplotlib)",
                 font=FONTS["tiny"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_card"]).pack(anchor="w", padx=16, pady=(0, 8))

        for lbl, val in zip(labels, values):
            row = tk.Frame(card, bg=COLORS["bg_card"])
            row.pack(fill="x", padx=16, pady=2)
            tk.Label(row, text=lbl, font=FONTS["body"],
                     fg=COLORS["text_primary"],
                     bg=COLORS["bg_card"]).pack(side="left")
            tk.Label(row, text=str(val), font=FONTS["body_bold"],
                     fg=COLORS["primary"],
                     bg=COLORS["bg_card"]).pack(side="right")

    def refresh(self):
        self._render_content()
