"""
Dashboard screen with stat cards and recent activity.
"""

import tkinter as tk
from database import get_connection
from theme import COLORS, FONTS
from widgets import StatCard, CardFrame


class DashboardScreen(tk.Frame):
    """Main dashboard with stats overview and recent transactions."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=COLORS["bg_main"])
        header.pack(fill="x", padx=24, pady=(20, 6))

        tk.Label(header, text="Dashboard", font=FONTS["heading_xl"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_main"]).pack(
            side="left")

        # ── Stat Cards Row ──
        stats_frame = tk.Frame(self, bg=COLORS["bg_main"])
        stats_frame.pack(fill="x", padx=24, pady=(10, 8))

        for i in range(4):
            stats_frame.columnconfigure(i, weight=1, uniform="stat")

        self.stat_products = StatCard(stats_frame, label="Total Products",
                                       value="0", icon="📦",
                                       accent_color=COLORS["primary"])
        self.stat_products.grid(row=0, column=0, sticky="nsew",
                                padx=(0, 8), pady=4)

        self.stat_lowstock = StatCard(stats_frame, label="Low Stock Alerts",
                                       value="0", icon="⚠️",
                                       accent_color=COLORS["danger"])
        self.stat_lowstock.grid(row=0, column=1, sticky="nsew",
                                padx=4, pady=4)

        self.stat_suppliers = StatCard(stats_frame, label="Suppliers",
                                        value="0", icon="🏭",
                                        accent_color=COLORS["success"])
        self.stat_suppliers.grid(row=0, column=2, sticky="nsew",
                                 padx=4, pady=4)

        self.stat_txns = StatCard(stats_frame, label="Total Transactions",
                                   value="0", icon="🔄",
                                   accent_color="#7C3AED")
        self.stat_txns.grid(row=0, column=3, sticky="nsew",
                            padx=(8, 0), pady=4)

        # ── Recent Activity ──
        activity_card = CardFrame(self)
        activity_card.pack(fill="both", expand=True, padx=24, pady=(8, 20))

        card_header = tk.Frame(activity_card, bg=COLORS["bg_card"])
        card_header.pack(fill="x", padx=16, pady=(14, 8))
        tk.Label(card_header, text="Recent Activity",
                 font=FONTS["heading_md"], fg=COLORS["text_primary"],
                 bg=COLORS["bg_card"]).pack(side="left")

        # Separator
        sep = tk.Frame(activity_card, bg=COLORS["border"], height=1)
        sep.pack(fill="x", padx=16)

        # Activity list container
        self.activity_frame = tk.Frame(activity_card, bg=COLORS["bg_card"])
        self.activity_frame.pack(fill="both", expand=True, padx=16, pady=8)

    def refresh(self):
        """Reload all dashboard data from DB."""
        conn = get_connection()
        cur = conn.cursor()

        # Total products
        cur.execute("SELECT COUNT(*) FROM products")
        self.stat_products.update_value(cur.fetchone()[0])

        # Low stock
        cur.execute("SELECT COUNT(*) FROM products WHERE quantity <= reorder_level")
        self.stat_lowstock.update_value(cur.fetchone()[0])

        # Suppliers
        cur.execute("SELECT COUNT(*) FROM suppliers")
        self.stat_suppliers.update_value(cur.fetchone()[0])

        # Total transactions
        cur.execute("SELECT COUNT(*) FROM transactions")
        self.stat_txns.update_value(cur.fetchone()[0])

        # Recent activity (last 15)
        cur.execute("""
            SELECT t.type, t.quantity, p.name, t.notes, t.created_at
            FROM transactions t
            JOIN products p ON t.product_id = p.id
            ORDER BY t.created_at DESC
            LIMIT 15
        """)
        txns = cur.fetchall()
        conn.close()

        # Clear old
        for w in self.activity_frame.winfo_children():
            w.destroy()

        if not txns:
            tk.Label(self.activity_frame, text="No transactions yet.",
                     font=FONTS["body"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_card"]).pack(pady=20)
            return

        for txn in txns:
            row = tk.Frame(self.activity_frame, bg=COLORS["bg_card"])
            row.pack(fill="x", pady=3)

            txn_type = txn["type"].upper()
            if txn_type == "IN":
                badge_bg = COLORS["success_bg"]
                badge_fg = COLORS["success"]
                symbol = "+"
            else:
                badge_bg = COLORS["danger_bg"]
                badge_fg = COLORS["danger"]
                symbol = "-"

            badge = tk.Label(row, text=f" {txn_type} ", font=FONTS["tiny"],
                             fg=badge_fg, bg=badge_bg)
            badge.pack(side="left", padx=(0, 8))

            desc = f"{symbol}{txn['quantity']} units — {txn['name']}"
            tk.Label(row, text=desc, font=FONTS["body"],
                     fg=COLORS["text_primary"],
                     bg=COLORS["bg_card"]).pack(side="left")

            tk.Label(row, text=txn["created_at"][:16],
                     font=FONTS["tiny"], fg=COLORS["text_muted"],
                     bg=COLORS["bg_card"]).pack(side="right")
