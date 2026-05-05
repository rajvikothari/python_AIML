"""
Stock Transactions screen: log stock in/out and view history.
"""

import tkinter as tk
from tkinter import messagebox
from database import get_connection
from theme import COLORS, FONTS
from widgets import CardFrame, StyledButton, StyledEntry, DataTable, SearchBar


class TransactionsScreen(tk.Frame):
    """Stock in/out transaction logging and history."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["bg_main"])
        header.pack(fill="x", padx=24, pady=(20, 10))

        tk.Label(header, text="Stock Transactions", font=FONTS["heading_xl"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_main"]).pack(
            side="left")

        btn_frame = tk.Frame(header, bg=COLORS["bg_main"])
        btn_frame.pack(side="right")

        StyledButton(btn_frame, text="📥 Stock In",
                     command=lambda: self._show_form("in"),
                     width=120, height=36,
                     bg=COLORS["success"]).pack(side="left", padx=(0, 8))

        StyledButton(btn_frame, text="📤 Stock Out",
                     command=lambda: self._show_form("out"),
                     width=120, height=36,
                     bg=COLORS["danger"]).pack(side="left")

        # Search
        search_row = tk.Frame(self, bg=COLORS["bg_main"])
        search_row.pack(fill="x", padx=24, pady=(0, 10))
        self.search_bar = SearchBar(search_row,
                                     placeholder="Search by product name...",
                                     on_search=self._on_search)
        self.search_bar.pack(fill="x")

        # Table
        table_card = CardFrame(self)
        table_card.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        columns = ("ID", "Date", "Type", "Product", "Quantity",
                   "User", "Notes")
        widths = (40, 130, 60, 150, 70, 100, 200)

        self.table = DataTable(table_card, columns=columns,
                                column_widths=widths)
        self.table.pack(fill="both", expand=True, padx=2, pady=2)

        self.form_overlay = None

    def _on_search(self, text):
        self._apply_filter()

    def _apply_filter(self):
        search = self.search_bar.get().lower()
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT t.id, t.created_at, t.type, p.name as product,
                   t.quantity, u.full_name as user_name, t.notes
            FROM transactions t
            JOIN products p ON t.product_id = p.id
            JOIN users u ON t.user_id = u.id
        """
        params = []
        if search:
            query += " WHERE LOWER(p.name) LIKE ?"
            params.append(f"%{search}%")

        query += " ORDER BY t.created_at DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        data = [(r["id"], r["created_at"][:16],
                 r["type"].upper(), r["product"],
                 r["quantity"], r["user_name"],
                 r["notes"] or "-") for r in rows]
        self.table.load_data(data)

    def refresh(self):
        self._apply_filter()

    def _show_form(self, txn_type):
        if self.form_overlay:
            self.form_overlay.destroy()

        self.form_overlay = tk.Frame(self, bg=COLORS["bg_main"])
        self.form_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        outer = tk.Frame(self.form_overlay, bg=COLORS["bg_main"])
        outer.place(relx=0.5, rely=0.5, anchor="center")

        accent = COLORS["success"] if txn_type == "in" else COLORS["danger"]
        title_text = "Stock In" if txn_type == "in" else "Stock Out"

        card = tk.Frame(outer, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1, padx=30, pady=24)
        card.pack()

        tk.Label(card, text=title_text, font=FONTS["heading_lg"],
                 fg=accent, bg=COLORS["bg_card"]).pack(
            anchor="w", pady=(0, 16))

        # Product dropdown
        prod_frame = tk.Frame(card, bg=COLORS["bg_card"])
        prod_frame.pack(fill="x", pady=(0, 10))
        tk.Label(prod_frame, text="Product", font=FONTS["small_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(
            anchor="w", pady=(0, 4))

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, quantity FROM products ORDER BY name")
        products = cur.fetchall()
        conn.close()

        self.prod_map = {f"{p['name']} (Qty: {p['quantity']})": p["id"]
                         for p in products}

        self.f_prod_var = tk.StringVar(
            value=list(self.prod_map.keys())[0] if self.prod_map else "")
        prod_opts = list(self.prod_map.keys()) or ["No Products"]
        self.f_prod_dd = tk.OptionMenu(prod_frame, self.f_prod_var,
                                        *prod_opts)
        self.f_prod_dd.config(font=FONTS["input"], bg=COLORS["bg_input"],
                               relief="flat", highlightthickness=1,
                               highlightbackground=COLORS["border"],
                               width=35)
        self.f_prod_dd.pack(fill="x")

        # Quantity
        self.f_qty = StyledEntry(card, label="Quantity",
                                  placeholder="Enter quantity", width=320)
        self.f_qty.pack(fill="x", pady=(0, 10))

        # Notes
        self.f_notes = StyledEntry(card, label="Notes (optional)",
                                    placeholder="Reason / reference",
                                    width=320)
        self.f_notes.pack(fill="x", pady=(0, 10))

        self._txn_type = txn_type

        btn_row = tk.Frame(card, bg=COLORS["bg_card"])
        btn_row.pack(fill="x", pady=(16, 0))

        StyledButton(btn_row, text="Cancel", command=self._hide_form,
                     width=100, height=36, bg="#94A3B8").pack(
            side="right", padx=(8, 0))

        StyledButton(btn_row, text="Submit", command=self._save_txn,
                     width=100, height=36,
                     bg=accent).pack(side="right")

    def _hide_form(self):
        if self.form_overlay:
            self.form_overlay.destroy()
            self.form_overlay = None

    def _save_txn(self):
        prod_label = self.f_prod_var.get()
        prod_id = self.prod_map.get(prod_label)
        qty_str = self.f_qty.get().strip()
        notes = self.f_notes.get().strip()

        if not prod_id:
            messagebox.showwarning("Missing", "Please select a product.")
            return

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror("Invalid", "Quantity must be a positive integer.")
            return

        conn = get_connection()
        cur = conn.cursor()

        # Check stock for OUT
        if self._txn_type == "out":
            cur.execute("SELECT quantity FROM products WHERE id=?", (prod_id,))
            current = cur.fetchone()["quantity"]
            if qty > current:
                conn.close()
                messagebox.showerror("Insufficient Stock",
                                     f"Only {current} units available.")
                return

        # Insert transaction
        user_id = self.app.current_user["id"]
        cur.execute("""
            INSERT INTO transactions (product_id, user_id, type, quantity, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (prod_id, user_id, self._txn_type, qty, notes))

        # Update product quantity
        if self._txn_type == "in":
            cur.execute("UPDATE products SET quantity = quantity + ? WHERE id = ?",
                        (qty, prod_id))
        else:
            cur.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?",
                        (qty, prod_id))

        conn.commit()
        conn.close()

        self._hide_form()
        self.refresh()
        action = "added to" if self._txn_type == "in" else "removed from"
        messagebox.showinfo("Success", f"{qty} units {action} stock.")
