"""
Profile & Settings screen: change password, view profile info.
"""

import tkinter as tk
from tkinter import messagebox
from database import get_connection, hash_password
from theme import COLORS, FONTS
from widgets import CardFrame, StyledButton, StyledEntry


class ProfileScreen(tk.Frame):
    """User profile and settings."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["bg_main"])
        header.pack(fill="x", padx=24, pady=(20, 10))

        tk.Label(header, text="Profile & Settings", font=FONTS["heading_xl"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_main"]).pack(
            side="left")

        # Content area
        self.content = tk.Frame(self, bg=COLORS["bg_main"])
        self.content.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    def refresh(self):
        for w in self.content.winfo_children():
            w.destroy()

        user = self.app.current_user

        # Profile card
        profile_card = CardFrame(self.content)
        profile_card.pack(fill="x", pady=(0, 16))

        inner = tk.Frame(profile_card, bg=COLORS["bg_card"], padx=24, pady=20)
        inner.pack(fill="x")

        # Avatar
        avatar_frame = tk.Frame(inner, bg=COLORS["primary"],
                                 width=64, height=64)
        avatar_frame.pack_propagate(False)
        avatar_frame.pack(anchor="w", pady=(0, 12))

        initials = "".join(
            [w[0].upper() for w in user["full_name"].split()[:2]])
        tk.Label(avatar_frame, text=initials,
                 font=("Segoe UI", 20, "bold"),
                 fg=COLORS["text_white"],
                 bg=COLORS["primary"]).place(relx=0.5, rely=0.5,
                                              anchor="center")

        tk.Label(inner, text=user["full_name"], font=FONTS["heading_lg"],
                 fg=COLORS["text_primary"],
                 bg=COLORS["bg_card"]).pack(anchor="w")

        tk.Label(inner, text=f"@{user['username']}  •  {user['role'].title()}",
                 font=FONTS["body"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_card"]).pack(anchor="w", pady=(2, 0))

        if user["email"]:
            tk.Label(inner, text=user["email"], font=FONTS["body"],
                     fg=COLORS["text_secondary"],
                     bg=COLORS["bg_card"]).pack(anchor="w", pady=(2, 0))

        # ── Edit Profile ──
        edit_card = CardFrame(self.content)
        edit_card.pack(fill="x", pady=(0, 16))

        edit_inner = tk.Frame(edit_card, bg=COLORS["bg_card"], padx=24,
                              pady=20)
        edit_inner.pack(fill="x")

        tk.Label(edit_inner, text="Edit Profile", font=FONTS["heading_md"],
                 fg=COLORS["text_primary"],
                 bg=COLORS["bg_card"]).pack(anchor="w", pady=(0, 12))

        self.f_name = StyledEntry(edit_inner, label="Full Name", width=350)
        self.f_name.pack(anchor="w", pady=(0, 10))
        self.f_name.set(user["full_name"])

        self.f_email = StyledEntry(edit_inner, label="Email", width=350)
        self.f_email.pack(anchor="w", pady=(0, 12))
        self.f_email.set(user["email"] or "")

        StyledButton(edit_inner, text="Update Profile",
                     command=self._update_profile,
                     width=140, height=36,
                     bg=COLORS["primary"]).pack(anchor="w")

        # ── Change Password ──
        pw_card = CardFrame(self.content)
        pw_card.pack(fill="x")

        pw_inner = tk.Frame(pw_card, bg=COLORS["bg_card"], padx=24, pady=20)
        pw_inner.pack(fill="x")

        tk.Label(pw_inner, text="Change Password", font=FONTS["heading_md"],
                 fg=COLORS["text_primary"],
                 bg=COLORS["bg_card"]).pack(anchor="w", pady=(0, 12))

        self.f_current_pw = StyledEntry(pw_inner, label="Current Password",
                                         show="●", width=350)
        self.f_current_pw.pack(anchor="w", pady=(0, 10))

        self.f_new_pw = StyledEntry(pw_inner, label="New Password",
                                     show="●", width=350)
        self.f_new_pw.pack(anchor="w", pady=(0, 10))

        self.f_confirm_pw = StyledEntry(pw_inner, label="Confirm New Password",
                                         show="●", width=350)
        self.f_confirm_pw.pack(anchor="w", pady=(0, 12))

        StyledButton(pw_inner, text="Change Password",
                     command=self._change_password,
                     width=160, height=36,
                     bg=COLORS["warning"]).pack(anchor="w")

    def _update_profile(self):
        name = self.f_name.get().strip()
        email = self.f_email.get().strip()

        if not name:
            messagebox.showwarning("Missing", "Name is required.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET full_name=?, email=? WHERE id=?",
                    (name, email, self.app.current_user["id"]))
        conn.commit()
        conn.close()

        # Update session
        self.app.current_user["full_name"] = name
        self.app.current_user["email"] = email
        self.app.update_sidebar_user()

        messagebox.showinfo("Success", "Profile updated.")

    def _change_password(self):
        current = self.f_current_pw.get().strip()
        new_pw = self.f_new_pw.get().strip()
        confirm = self.f_confirm_pw.get().strip()

        if not all([current, new_pw, confirm]):
            messagebox.showwarning("Missing", "Fill in all password fields.")
            return

        if new_pw != confirm:
            messagebox.showerror("Mismatch", "New passwords don't match.")
            return

        if len(new_pw) < 4:
            messagebox.showwarning("Weak", "At least 4 characters required.")
            return

        # Verify current
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE id=?",
                    (self.app.current_user["id"],))
        row = cur.fetchone()

        if row["password"] != hash_password(current):
            conn.close()
            messagebox.showerror("Incorrect",
                                 "Current password is incorrect.")
            return

        cur.execute("UPDATE users SET password=? WHERE id=?",
                    (hash_password(new_pw), self.app.current_user["id"]))
        conn.commit()
        conn.close()

        self.f_current_pw.clear()
        self.f_new_pw.clear()
        self.f_confirm_pw.clear()

        messagebox.showinfo("Success", "Password changed successfully.")
