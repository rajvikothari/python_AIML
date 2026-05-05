"""
Categories management screen: list, add, edit, delete.
"""

import tkinter as tk
from tkinter import messagebox
from database import get_connection
from theme import COLORS, FONTS, CATEGORY_COLORS
from widgets import CardFrame, StyledButton, StyledEntry, DataTable


class CategoriesScreen(tk.Frame):
    """Category management with CRUD."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self.editing_id = None
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["bg_main"])
        header.pack(fill="x", padx=24, pady=(20, 10))

        tk.Label(header, text="Categories", font=FONTS["heading_xl"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_main"]).pack(
            side="left")

        StyledButton(header, text="＋ Add Category",
                     command=self._show_form,
                     width=150, height=36,
                     bg=COLORS["primary"]).pack(side="right")

        # Table
        table_card = CardFrame(self)
        table_card.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        columns = ("ID", "Name", "Color", "Description", "Product Count")
        widths = (50, 160, 80, 250, 100)

        self.table = DataTable(table_card, columns=columns,
                                column_widths=widths)
        self.table.pack(fill="both", expand=True, padx=2, pady=2)

        # Action buttons
        btn_row = tk.Frame(self, bg=COLORS["bg_main"])
        btn_row.pack(fill="x", padx=24, pady=(0, 16))

        StyledButton(btn_row, text="✏️ Edit", command=self._edit_selected,
                     width=100, height=32,
                     bg=COLORS["warning"]).pack(side="left", padx=(0, 8))

        StyledButton(btn_row, text="🗑️ Delete", command=self._delete_selected,
                     width=100, height=32,
                     bg=COLORS["danger"]).pack(side="left")

        self.form_overlay = None

    def refresh(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id, c.name, c.color, c.description,
                   COUNT(p.id) as product_count
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id
            ORDER BY c.name
        """)
        rows = cur.fetchall()
        conn.close()

        data = [(r["id"], r["name"], r["color"],
                 r["description"] or "-", r["product_count"]) for r in rows]
        self.table.load_data(data)

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

        title = "Edit Category" if edit_data else "Add New Category"
        tk.Label(card, text=title, font=FONTS["heading_lg"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(
            anchor="w", pady=(0, 16))

        self.f_name = StyledEntry(card, label="Category Name",
                                   placeholder="e.g. Electronics", width=300)
        self.f_name.pack(fill="x", pady=(0, 10))

        self.f_desc = StyledEntry(card, label="Description",
                                   placeholder="Brief description", width=300)
        self.f_desc.pack(fill="x", pady=(0, 10))

        # Color picker
        color_frame = tk.Frame(card, bg=COLORS["bg_card"])
        color_frame.pack(fill="x", pady=(0, 10))
        tk.Label(color_frame, text="Color", font=FONTS["small_bold"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(
            anchor="w", pady=(0, 4))

        self.selected_color = tk.StringVar(value=CATEGORY_COLORS[0][0])
        color_row = tk.Frame(color_frame, bg=COLORS["bg_card"])
        color_row.pack(anchor="w")

        for fg_col, bg_col in CATEGORY_COLORS:
            btn = tk.Canvas(color_row, width=28, height=28,
                            bg=COLORS["bg_card"], highlightthickness=0,
                            cursor="hand2")
            btn.create_oval(4, 4, 24, 24, fill=fg_col, outline="")
            btn.pack(side="left", padx=2)
            btn.bind("<Button-1>",
                     lambda e, c=fg_col: self.selected_color.set(c))

        if edit_data:
            self.editing_id = edit_data[0]
            self.f_name.set(str(edit_data[1]))
            self.selected_color.set(edit_data[2])
            if edit_data[3] != "-":
                self.f_desc.set(str(edit_data[3]))
        else:
            self.editing_id = None

        # Buttons
        btn_row = tk.Frame(card, bg=COLORS["bg_card"])
        btn_row.pack(fill="x", pady=(16, 0))

        StyledButton(btn_row, text="Cancel", command=self._hide_form,
                     width=100, height=36,
                     bg="#94A3B8").pack(side="right", padx=(8, 0))

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
        desc = self.f_desc.get().strip()
        color = self.selected_color.get()

        if not name:
            messagebox.showwarning("Missing", "Category name is required.")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            if self.editing_id:
                cur.execute("""
                    UPDATE categories SET name=?, color=?, description=?
                    WHERE id=?
                """, (name, color, desc, self.editing_id))
            else:
                cur.execute("""
                    INSERT INTO categories (name, color, description)
                    VALUES (?, ?, ?)
                """, (name, color, desc))
            conn.commit()
            self._hide_form()
            self.refresh()
        except Exception as e:
            if "UNIQUE" in str(e):
                messagebox.showerror("Duplicate", "Category name already exists.")
            else:
                messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def _edit_selected(self):
        sel = self.table.get_selected()
        if not sel:
            messagebox.showinfo("No Selection", "Select a category to edit.")
            return
        self._show_form(edit_data=sel)

    def _delete_selected(self):
        sel = self.table.get_selected()
        if not sel:
            messagebox.showinfo("No Selection", "Select a category to delete.")
            return
        if not messagebox.askyesno("Confirm", f"Delete '{sel[1]}'?"):
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM categories WHERE id = ?", (sel[0],))
        conn.commit()
        conn.close()
        self.refresh()
