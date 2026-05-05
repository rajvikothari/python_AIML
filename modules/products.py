"""
Products management screen: list, add, edit, delete, search.
"""

import tkinter as tk
from tkinter import messagebox
from database import get_connection
from theme import COLORS, FONTS, CATEGORY_COLORS
from widgets import CardFrame, StyledButton, StyledEntry, DataTable, SearchBar


class ProductsScreen(tk.Frame):
    """Product management with full CRUD operations."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self.editing_id = None
        self._build_ui()

    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self, bg=COLORS["bg_main"])
        header.pack(fill="x", padx=24, pady=(20, 10))

        tk.Label(header, text="Products", font=FONTS["heading_xl"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_main"]).pack(
            side="left")

        StyledButton(header, text="＋ Add Product",
                     command=self._show_form,
                     width=140, height=36,
                     bg=COLORS["primary"]).pack(side="right")

        # ── Search & Filter ──
        filter_row = tk.Frame(self, bg=COLORS["bg_main"])
        filter_row.pack(fill="x", padx=24, pady=(0, 10))

        self.search_bar = SearchBar(filter_row, placeholder="Search products...",
                                     on_search=self._on_search)
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Category filter
        self.cat_var = tk.StringVar(value="All Categories")
        self.cat_dropdown = tk.OptionMenu(filter_row, self.cat_var,
                                           "All Categories")
        self.cat_dropdown.config(font=FONTS["small"], bg=COLORS["bg_input"],
                                  fg=COLORS["text_primary"],
                                  highlightthickness=1,
                                  highlightbackground=COLORS["border"],
                                  relief="flat", width=16)
        self.cat_dropdown.pack(side="right")

        # ── Table ──
        table_card = CardFrame(self)
        table_card.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        columns = ("ID", "Name", "SKU", "Category", "Supplier",
                   "Price", "Qty", "Reorder Lvl", "Location")
        widths = (40, 150, 80, 100, 120, 70, 50, 80, 90)

        self.table = DataTable(table_card, columns=columns,
                                column_widths=widths)
        self.table.pack(fill="both", expand=True, padx=2, pady=2)

        # ── Action Buttons (bottom) ──
        btn_row = tk.Frame(self, bg=COLORS["bg_main"])
        btn_row.pack(fill="x", padx=24, pady=(0, 16))

        StyledButton(btn_row, text="✏️ Edit", command=self._edit_selected,
                     width=100, height=32,
                     bg=COLORS["warning"]).pack(side="left", padx=(0, 8))

        StyledButton(btn_row, text="🗑️ Delete", command=self._delete_selected,
                     width=100, height=32,
                     bg=COLORS["danger"]).pack(side="left")

        # ── Form (hidden by default) ──
        self.form_overlay = None

    def _load_categories_dropdown(self):
        """Populate category filter dropdown."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM categories ORDER BY name")
        cats = [r["name"] for r in cur.fetchall()]
        conn.close()

        menu = self.cat_dropdown["menu"]
        menu.delete(0, "end")
        menu.add_command(label="All Categories",
                         command=lambda: (self.cat_var.set("All Categories"),
                                          self._apply_filter()))
        for c in cats:
            menu.add_command(label=c,
                             command=lambda v=c: (self.cat_var.set(v),
                                                   self._apply_filter()))

    def _on_search(self, text):
        self._apply_filter()

    def _apply_filter(self):
        search = self.search_bar.get().lower()
        cat = self.cat_var.get()

        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT p.id, p.name, p.sku,
                   COALESCE(c.name, '-') as category,
                   COALESCE(s.name, '-') as supplier,
                   p.price, p.quantity, p.reorder_level, p.location
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (LOWER(p.name) LIKE ? OR LOWER(p.sku) LIKE ?)"
            params += [f"%{search}%", f"%{search}%"]

        if cat != "All Categories":
            query += " AND c.name = ?"
            params.append(cat)

        query += " ORDER BY p.name"
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        data = []
        for r in rows:
            data.append((r["id"], r["name"], r["sku"], r["category"],
                         r["supplier"], f"${r['price']:.2f}",
                         r["quantity"], r["reorder_level"],
                         r["location"] or "-"))
        self.table.load_data(data)

    def refresh(self):
        self._load_categories_dropdown()
        self._apply_filter()

    def _show_form(self, edit_data=None):
        """Show add/edit form as overlay."""
        if self.form_overlay:
            self.form_overlay.destroy()

        self.form_overlay = tk.Frame(self, bg=COLORS["bg_main"])
        self.form_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Scrollable container
        outer = tk.Frame(self.form_overlay, bg=COLORS["bg_main"])
        outer.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(outer, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1, padx=30, pady=24)
        card.pack()

        title = "Edit Product" if edit_data else "Add New Product"
        tk.Label(card, text=title, font=FONTS["heading_lg"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(
            anchor="w", pady=(0, 16))

        # Two-column layout
        form_grid = tk.Frame(card, bg=COLORS["bg_card"])
        form_grid.pack(fill="x")

        left = tk.Frame(form_grid, bg=COLORS["bg_card"])
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        right = tk.Frame(form_grid, bg=COLORS["bg_card"])
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        # Fields
        self.f_name = StyledEntry(left, label="Product Name",
                                   placeholder="e.g. Wireless Mouse", width=240)
        self.f_name.pack(fill="x", pady=(0, 10))

        self.f_sku = StyledEntry(left, label="SKU Code",
                                  placeholder="e.g. WM-1042", width=240)
        self.f_sku.pack(fill="x", pady=(0, 10))

        self.f_price = StyledEntry(left, label="Price ($)",
                                    placeholder="0.00", width=240)
        self.f_price.pack(fill="x", pady=(0, 10))

        self.f_qty = StyledEntry(left, label="Quantity",
                                  placeholder="0", width=240)
        self.f_qty.pack(fill="x", pady=(0, 10))

        self.f_reorder = StyledEntry(right, label="Reorder Level",
                                      placeholder="10", width=240)
        self.f_reorder.pack(fill="x", pady=(0, 10))

        self.f_location = StyledEntry(right, label="Location",
                                       placeholder="e.g. Shelf A1", width=240)
        self.f_location.pack(fill="x", pady=(0, 10))

        # Category dropdown
        cat_frame = tk.Frame(right, bg=COLORS["bg_card"])
        cat_frame.pack(fill="x", pady=(0, 10))
        tk.Label(cat_frame, text="Category", font=FONTS["small_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(
            anchor="w", pady=(0, 4))

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM categories ORDER BY name")
        cats = cur.fetchall()
        cur.execute("SELECT id, name FROM suppliers ORDER BY name")
        sups = cur.fetchall()
        conn.close()

        self.cat_map = {c["name"]: c["id"] for c in cats}
        self.sup_map = {s["name"]: s["id"] for s in sups}

        self.f_cat_var = tk.StringVar(
            value=list(self.cat_map.keys())[0] if self.cat_map else "")
        cat_opts = list(self.cat_map.keys()) or ["None"]
        self.f_cat_dd = tk.OptionMenu(cat_frame, self.f_cat_var, *cat_opts)
        self.f_cat_dd.config(font=FONTS["input"], bg=COLORS["bg_input"],
                              relief="flat", highlightthickness=1,
                              highlightbackground=COLORS["border"])
        self.f_cat_dd.pack(fill="x")

        # Supplier dropdown
        sup_frame = tk.Frame(right, bg=COLORS["bg_card"])
        sup_frame.pack(fill="x", pady=(0, 10))
        tk.Label(sup_frame, text="Supplier", font=FONTS["small_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(
            anchor="w", pady=(0, 4))

        self.f_sup_var = tk.StringVar(
            value=list(self.sup_map.keys())[0] if self.sup_map else "")
        sup_opts = list(self.sup_map.keys()) or ["None"]
        self.f_sup_dd = tk.OptionMenu(sup_frame, self.f_sup_var, *sup_opts)
        self.f_sup_dd.config(font=FONTS["input"], bg=COLORS["bg_input"],
                              relief="flat", highlightthickness=1,
                              highlightbackground=COLORS["border"])
        self.f_sup_dd.pack(fill="x")

        # Pre-fill if editing
        if edit_data:
            self.editing_id = edit_data[0]
            self.f_name.set(str(edit_data[1]))
            self.f_sku.set(str(edit_data[2]))
            if edit_data[3] in self.cat_map:
                self.f_cat_var.set(edit_data[3])
            if edit_data[4] in self.sup_map:
                self.f_sup_var.set(edit_data[4])
            price_str = str(edit_data[5]).replace("$", "")
            self.f_price.set(price_str)
            self.f_qty.set(str(edit_data[6]))
            self.f_reorder.set(str(edit_data[7]))
            self.f_location.set(str(edit_data[8]) if edit_data[8] != "-" else "")
        else:
            self.editing_id = None

        # Buttons
        btn_row = tk.Frame(card, bg=COLORS["bg_card"])
        btn_row.pack(fill="x", pady=(16, 0))

        StyledButton(btn_row, text="Cancel", command=self._hide_form,
                     width=100, height=36,
                     bg="#94A3B8", fg=COLORS["text_white"]).pack(
            side="right", padx=(8, 0))

        save_text = "Update" if edit_data else "Save"
        StyledButton(btn_row, text=save_text, command=self._save_product,
                     width=100, height=36,
                     bg=COLORS["primary"]).pack(side="right")

    def _hide_form(self):
        if self.form_overlay:
            self.form_overlay.destroy()
            self.form_overlay = None
        self.editing_id = None

    def _save_product(self):
        name = self.f_name.get().strip()
        sku = self.f_sku.get().strip()
        cat_name = self.f_cat_var.get()
        sup_name = self.f_sup_var.get()
        price = self.f_price.get().strip()
        qty = self.f_qty.get().strip()
        reorder = self.f_reorder.get().strip()
        location = self.f_location.get().strip()

        if not name or not sku:
            messagebox.showwarning("Missing Fields",
                                   "Product name and SKU are required.")
            return

        try:
            price = float(price) if price else 0.0
            qty = int(qty) if qty else 0
            reorder = int(reorder) if reorder else 10
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Price must be a number, Qty and Reorder "
                                 "must be integers.")
            return

        cat_id = self.cat_map.get(cat_name)
        sup_id = self.sup_map.get(sup_name)

        conn = get_connection()
        cur = conn.cursor()

        try:
            if self.editing_id:
                cur.execute("""
                    UPDATE products SET name=?, sku=?, category_id=?,
                    supplier_id=?, price=?, quantity=?, reorder_level=?,
                    location=? WHERE id=?
                """, (name, sku, cat_id, sup_id, price, qty, reorder,
                      location, self.editing_id))
            else:
                cur.execute("""
                    INSERT INTO products (name, sku, category_id, supplier_id,
                    price, quantity, reorder_level, location)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, sku, cat_id, sup_id, price, qty, reorder,
                      location))

            conn.commit()
            self._hide_form()
            self.refresh()
            action = "updated" if self.editing_id else "added"
            messagebox.showinfo("Success", f"Product {action} successfully!")

        except Exception as e:
            if "UNIQUE constraint" in str(e):
                messagebox.showerror("Duplicate SKU",
                                     "A product with that SKU already exists.")
            else:
                messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def _edit_selected(self):
        sel = self.table.get_selected()
        if not sel:
            messagebox.showinfo("No Selection",
                                "Please select a product to edit.")
            return
        self._show_form(edit_data=sel)

    def _delete_selected(self):
        sel = self.table.get_selected()
        if not sel:
            messagebox.showinfo("No Selection",
                                "Please select a product to delete.")
            return

        if not messagebox.askyesno("Confirm Delete",
                                    f"Delete product '{sel[1]}'?"):
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id = ?", (sel[0],))
        conn.commit()
        conn.close()
        self.refresh()
        messagebox.showinfo("Deleted", "Product deleted successfully.")
