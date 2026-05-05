"""
Authentication screens: Login and Signup.
"""

import tkinter as tk
from tkinter import messagebox
from database import get_connection, hash_password
from theme import COLORS, FONTS
from widgets import StyledEntry, StyledButton


class LoginScreen(tk.Frame):
    """Login screen with username/password fields."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build_ui()

    def _build_ui(self):
        # Center container
        center = tk.Frame(self, bg=COLORS["bg_main"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Card
        card = tk.Frame(center, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1, padx=40, pady=36)
        card.pack()

        # Logo
        logo_frame = tk.Frame(card, bg=COLORS["primary"], width=52, height=52)
        logo_frame.pack_propagate(False)
        logo_frame.pack(pady=(0, 12))
        tk.Label(logo_frame, text="IMS", font=("Segoe UI", 14, "bold"),
                 fg=COLORS["text_white"], bg=COLORS["primary"]).place(
            relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(card, text="Welcome back", font=FONTS["heading_lg"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(
            pady=(0, 2))
        tk.Label(card, text="Sign in to your account", font=FONTS["small"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(
            pady=(0, 24))

        # Username
        self.username_entry = StyledEntry(card, label="Username",
                                          placeholder="Enter username",
                                          width=280)
        self.username_entry.pack(fill="x", pady=(0, 12))

        # Password
        self.password_entry = StyledEntry(card, label="Password",
                                          placeholder="Enter password",
                                          show="●", width=280)
        self.password_entry.pack(fill="x", pady=(0, 20))

        # Login button
        StyledButton(card, text="Sign In", command=self._login,
                     width=280, height=40,
                     bg=COLORS["primary"]).pack(pady=(0, 16))

        # Signup link
        link_frame = tk.Frame(card, bg=COLORS["bg_card"])
        link_frame.pack()
        tk.Label(link_frame, text="Don't have an account? ",
                 font=FONTS["small"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_card"]).pack(side="left")
        signup_lbl = tk.Label(link_frame, text="Sign up",
                              font=FONTS["small_bold"],
                              fg=COLORS["primary"], bg=COLORS["bg_card"],
                              cursor="hand2")
        signup_lbl.pack(side="left")
        signup_lbl.bind("<Button-1>", lambda e: self.app.show_signup())

        # Default credentials hint
        hint = tk.Frame(self, bg=COLORS["bg_main"])
        hint.place(relx=0.5, rely=0.92, anchor="center")
        tk.Label(hint, text="Default logins → admin/admin123  •  staff/staff123",
                 font=FONTS["tiny"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_main"]).pack()

    def _login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing Fields",
                                   "Please enter both username and password.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password)))
        user = cursor.fetchone()
        conn.close()

        if user is None:
            messagebox.showerror("Login Failed",
                                 "Invalid username or password.")
            return

        if user["status"] == "pending":
            messagebox.showinfo("Account Pending",
                                "Your account is pending admin approval.")
            return

        if user["status"] == "inactive":
            messagebox.showinfo("Account Inactive",
                                "Your account has been deactivated. "
                                "Contact an admin.")
            return

        # Success
        self.app.current_user = dict(user)
        self.app.show_main()


class SignupScreen(tk.Frame):
    """Signup screen for new user registration."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.app = app
        self._build_ui()

    def _build_ui(self):
        center = tk.Frame(self, bg=COLORS["bg_main"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(center, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1, padx=40, pady=30)
        card.pack()

        # Title
        tk.Label(card, text="Create Account", font=FONTS["heading_lg"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(
            pady=(0, 2))
        tk.Label(card, text="Register for a new staff account",
                 font=FONTS["small"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_card"]).pack(pady=(0, 20))

        # Full Name
        self.name_entry = StyledEntry(card, label="Full Name",
                                       placeholder="Enter full name",
                                       width=300)
        self.name_entry.pack(fill="x", pady=(0, 10))

        # Email
        self.email_entry = StyledEntry(card, label="Email",
                                        placeholder="Enter email",
                                        width=300)
        self.email_entry.pack(fill="x", pady=(0, 10))

        # Username
        self.username_entry = StyledEntry(card, label="Username",
                                           placeholder="Choose a username",
                                           width=300)
        self.username_entry.pack(fill="x", pady=(0, 10))

        # Password
        self.password_entry = StyledEntry(card, label="Password",
                                           placeholder="Choose a password",
                                           show="●", width=300)
        self.password_entry.pack(fill="x", pady=(0, 10))

        # Confirm Password
        self.confirm_entry = StyledEntry(card, label="Confirm Password",
                                          placeholder="Re-enter password",
                                          show="●", width=300)
        self.confirm_entry.pack(fill="x", pady=(0, 20))

        # Signup button
        StyledButton(card, text="Create Account", command=self._signup,
                     width=300, height=40,
                     bg=COLORS["primary"]).pack(pady=(0, 14))

        # Back to login
        link_frame = tk.Frame(card, bg=COLORS["bg_card"])
        link_frame.pack()
        tk.Label(link_frame, text="Already have an account? ",
                 font=FONTS["small"], fg=COLORS["text_secondary"],
                 bg=COLORS["bg_card"]).pack(side="left")
        login_lbl = tk.Label(link_frame, text="Sign in",
                             font=FONTS["small_bold"],
                             fg=COLORS["primary"], bg=COLORS["bg_card"],
                             cursor="hand2")
        login_lbl.pack(side="left")
        login_lbl.bind("<Button-1>", lambda e: self.app.show_login())

    def _signup(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if not all([name, username, password, confirm]):
            messagebox.showwarning("Missing Fields",
                                   "Please fill in all required fields.")
            return

        if password != confirm:
            messagebox.showerror("Password Mismatch",
                                 "Passwords do not match.")
            return

        if len(password) < 4:
            messagebox.showwarning("Weak Password",
                                   "Password must be at least 4 characters.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # Check unique username
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            messagebox.showerror("Username Taken",
                                 "That username is already in use.")
            return

        cursor.execute("""
            INSERT INTO users (username, password, full_name, email, role, status)
            VALUES (?, ?, ?, ?, 'staff', 'pending')
        """, (username, hash_password(password), name, email))

        conn.commit()
        conn.close()

        messagebox.showinfo("Registration Successful",
                            "Account created! An admin must approve your "
                            "account before you can sign in.")
        self.app.show_login()
