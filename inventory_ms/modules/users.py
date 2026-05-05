"""
User Management screen (Admin only): view, approve, change roles, deactivate.
"""

import tkinter as tk
from tkinter import messagebox
from database import get_connection
from theme import COLORS, FONTS
from widgets import CardFrame, StyledButton, DataTable


class UsersScreen(tk.Frame):
    """Admin-only user management."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["bg_main"])
        header.pack(fill="x", padx=24, pady=(20, 10))

        tk.Label(header, text="User Management", font=FONTS["heading_xl"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_main"]).pack(
            side="left")

        # Table
        table_card = CardFrame(self)
        table_card.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        columns = ("ID", "Username", "Full Name", "Email", "Role",
                   "Status", "Created")
        widths = (40, 110, 140, 170, 70, 80, 130)

        self.table = DataTable(table_card, columns=columns,
                                column_widths=widths)
        self.table.pack(fill="both", expand=True, padx=2, pady=2)

        # Action buttons
        btn_row = tk.Frame(self, bg=COLORS["bg_main"])
        btn_row.pack(fill="x", padx=24, pady=(0, 16))

        StyledButton(btn_row, text="✅ Approve",
                     command=self._approve_user,
                     width=110, height=32,
                     bg=COLORS["success"]).pack(side="left", padx=(0, 8))

        StyledButton(btn_row, text="🔄 Toggle Role",
                     command=self._toggle_role,
                     width=120, height=32,
                     bg=COLORS["info"]).pack(side="left", padx=(0, 8))

        StyledButton(btn_row, text="🚫 Deactivate",
                     command=self._deactivate_user,
                     width=120, height=32,
                     bg=COLORS["warning"]).pack(side="left", padx=(0, 8))

        StyledButton(btn_row, text="♻️ Reactivate",
                     command=self._reactivate_user,
                     width=120, height=32,
                     bg="#7C3AED").pack(side="left", padx=(0, 8))

        StyledButton(btn_row, text="🗑️ Delete",
                     command=self._delete_user,
                     width=100, height=32,
                     bg=COLORS["danger"]).pack(side="left")

    def refresh(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, username, full_name, email, role, status, created_at
            FROM users ORDER BY created_at DESC
        """)
        rows = cur.fetchall()
        conn.close()

        data = [(r["id"], r["username"], r["full_name"],
                 r["email"] or "-", r["role"].title(),
                 r["status"].title(), r["created_at"][:16]) for r in rows]
        self.table.load_data(data)

    def _get_selected_user(self):
        sel = self.table.get_selected()
        if not sel:
            messagebox.showinfo("No Selection", "Please select a user.")
            return None
        return sel

    def _approve_user(self):
        sel = self._get_selected_user()
        if not sel:
            return
        if sel[5] != "Pending":
            messagebox.showinfo("Info", "User is not in pending status.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET status='active' WHERE id=?", (sel[0],))
        conn.commit()
        conn.close()
        self.refresh()
        messagebox.showinfo("Approved", f"User '{sel[1]}' is now active.")

    def _toggle_role(self):
        sel = self._get_selected_user()
        if not sel:
            return

        if sel[1] == "admin" and sel[0] == 1:
            messagebox.showwarning("Cannot Change",
                                   "Cannot change the default admin's role.")
            return

        current_role = sel[4].lower()
        new_role = "admin" if current_role == "staff" else "staff"

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET role=? WHERE id=?", (new_role, sel[0]))
        conn.commit()
        conn.close()
        self.refresh()
        messagebox.showinfo("Role Changed",
                            f"'{sel[1]}' is now {new_role.title()}.")

    def _deactivate_user(self):
        sel = self._get_selected_user()
        if not sel:
            return
        if sel[0] == self.app.current_user["id"]:
            messagebox.showwarning("Cannot Deactivate",
                                   "You cannot deactivate yourself.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET status='inactive' WHERE id=?",
                    (sel[0],))
        conn.commit()
        conn.close()
        self.refresh()

    def _reactivate_user(self):
        sel = self._get_selected_user()
        if not sel:
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET status='active' WHERE id=?", (sel[0],))
        conn.commit()
        conn.close()
        self.refresh()

    def _delete_user(self):
        sel = self._get_selected_user()
        if not sel:
            return
        if sel[0] == self.app.current_user["id"]:
            messagebox.showwarning("Cannot Delete",
                                   "You cannot delete your own account.")
            return

        if not messagebox.askyesno("Confirm",
                                    f"Permanently delete user '{sel[1]}'?"):
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (sel[0],))
        conn.commit()
        conn.close()
        self.refresh()
