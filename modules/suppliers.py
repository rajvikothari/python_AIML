"""
Suppliers management screen: list, add, edit, delete.
"""

import tkinter as tk
from tkinter import messagebox
from database import get_connection
from theme import COLORS, FONTS
from widgets import CardFrame, StyledButton, StyledEntry, DataTable, SearchBar


class SuppliersScreen(tk.Frame):
    """Supplier management with CRUD."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self.editing_id = None
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["bg_main"])
        header.pack(fill="x", padx=24, pady=(20, 10))

        tk.Label(header, text="Suppliers", font=FONTS["heading_xl"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_main"]).pack(
            side="left")

        StyledButton(header, text="＋ Add Supplier",
                     command=self._show_form,
                     width=140, height=36,
                     bg=COLORS["primary"]).pack(side="right")

        # Search
        search_row = tk.Frame(self, bg=COLORS["bg_main"])
        search_row.pack(fill="x", padx=24, pady=(0, 10))
        self.search_bar = SearchBar(search_row,
                                     placeholder="Search suppliers...",
                                     on_search=self._on_search)
        self.search_bar.pack(fill="x")

        # Table
        table_card = CardFrame(self)
        table_card.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        columns = ("ID", "Name", "Contact Person", "Phone", "Email",
                   "Products Supplied")
        widths = (40, 150, 130, 110, 160, 110)

        self.table = DataTable(table_card, columns=columns,
                                column_widths=widths)
        self.table.pack(fill="both", expand=True, padx=2, pady=2)

        btn_row = tk.Frame(self, bg=COLORS["bg_main"])
        btn_row.pack(fill="x", padx=24, pady=(0, 16))

        StyledButton(btn_row, text="✏️ Edit", command=self._edit_selected,
                     width=100, height=32,
                     bg=COLORS["warning"]).pack(side="left", padx=(0, 8))

        StyledButton(btn_row, text="🗑️ Delete", command=self._delete_selected,
                     width=100, height=32,
                     bg=COLORS["danger"]).pack(side="left")

        self.form_overlay = None

    def _on_search(self, text):
        self._apply_filter()

    def _apply_filter(self):
        search = self.search_bar.get().lower()
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT s.id, s.name, s.contact_person, s.phone, s.email,
                   COUNT(p.id) as prod_count
            FROM suppliers s
            LEFT JOIN products p ON s.id = p.supplier_id
        """
        params = []
        if search:
            query += " WHERE LOWER(s.name) LIKE ? OR LOWER(s.contact_person) LIKE ?"
            params += [f"%{search}%", f"%{search}%"]

        query += " GROUP BY s.id ORDER BY s.name"
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        data = [(r["id"], r["name"], r["contact_person"] or "-",
                 r["phone"] or "-", r["email"] or "-",
                 r["prod_count"]) for r in rows]
        self.table.load_data(data)

    def refresh(self):
        self._apply_filter()

    def _show_form(self, edit_data=None):
        if self.form_overlay:
            self.form_overlay.destroy()

        self.form_overlay = tk.Frame(self, bg=COLORS["bg_main"])
        self.form_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        outer = tk.Frame(self.form_overlay, bg=COLORS["bg_main"])
        outer.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(outer, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1, padx=30, pady=24)
        card.pack()

        title = "Edit Supplier" if edit_data else "Add New Supplier"
        tk.Label(card, text=title, font=FONTS["heading_lg"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(
            anchor="w", pady=(0, 16))

        self.f_name = StyledEntry(card, label="Company Name",
                                   placeholder="e.g. TechWorld Supplies",
                                   width=320)
        self.f_name.pack(fill="x", pady=(0, 10))

        self.f_contact = StyledEntry(card, label="Contact Person",
                                      placeholder="e.g. Alice Chen", width=320)
        self.f_contact.pack(fill="x", pady=(0, 10))

        self.f_phone = StyledEntry(card, label="Phone",
                                    placeholder="+1-555-0101", width=320)
        self.f_phone.pack(fill="x", pady=(0, 10))

        self.f_email = StyledEntry(card, label="Email",
                                    placeholder="contact@company.com",
                                    width=320)
        self.f_email.pack(fill="x", pady=(0, 10))

        self.f_address = StyledEntry(card, label="Address",
                                      placeholder="Full address", width=320)
        self.f_address.pack(fill="x", pady=(0, 10))

        if edit_data:
            self.editing_id = edit_data[0]
            self.f_name.set(str(edit_data[1]))
            if edit_data[2] != "-":
                self.f_contact.set(str(edit_data[2]))
            if edit_data[3] != "-":
                self.f_phone.set(str(edit_data[3]))
            if edit_data[4] != "-":
                self.f_email.set(str(edit_data[4]))
            # Fetch address from DB
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT address FROM suppliers WHERE id=?",
                        (edit_data[0],))
            row = cur.fetchone()
            conn.close()
            if row and row["address"]:
                self.f_address.set(row["address"])
        else:
            self.editing_id = None

        btn_row = tk.Frame(card, bg=COLORS["bg_card"])
        btn_row.pack(fill="x", pady=(16, 0))

        StyledButton(btn_row, text="Cancel", command=self._hide_form,
                     width=100, height=36, bg="#94A3B8").pack(
            side="right", padx=(8, 0))

        save_text = "Update" if edit_data else "Save"
        StyledButton(btn_row, text=save_text, command=self._save,
                     width=100, height=36,
                     bg=COLORS["primary"]).pack(side="right")

    def _hide_form(self):
        if self.form_overlay:
            self.form_overlay.destroy()
            self.form_overlay = None
        self.editing_id = None

    def _save(self):
        name = self.f_name.get().strip()
        contact = self.f_contact.get().strip()
        phone = self.f_phone.get().strip()
        email = self.f_email.get().strip()
        address = self.f_address.get().strip()

        if not name:
            messagebox.showwarning("Missing", "Company name is required.")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            if self.editing_id:
                cur.execute("""
                    UPDATE suppliers SET name=?, contact_person=?, phone=?,
                    email=?, address=? WHERE id=?
                """, (name, contact, phone, email, address, self.editing_id))
            else:
                cur.execute("""
                    INSERT INTO suppliers (name, contact_person, phone,
                    email, address) VALUES (?, ?, ?, ?, ?)
                """, (name, contact, phone, email, address))
            conn.commit()
            self._hide_form()
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def _edit_selected(self):
        sel = self.table.get_selected()
        if not sel:
            messagebox.showinfo("No Selection", "Select a supplier to edit.")
            return
        self._show_form(edit_data=sel)

    def _delete_selected(self):
        sel = self.table.get_selected()
        if not sel:
            messagebox.showinfo("No Selection",
                                "Select a supplier to delete.")
            return
        if not messagebox.askyesno("Confirm", f"Delete '{sel[1]}'?"):
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM suppliers WHERE id = ?", (sel[0],))
        conn.commit()
        conn.close()
        self.refresh()
