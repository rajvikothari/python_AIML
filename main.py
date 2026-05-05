"""
Inventory Management System — Main Application
Run this file to start the application.
"""

import tkinter as tk
from database import initialize_database
from theme import COLORS, FONTS, SIDEBAR_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT
from widgets import StyledButton

from modules.auth import LoginScreen, SignupScreen
from modules.dashboard import DashboardScreen
from modules.products import ProductsScreen
from modules.categories import CategoriesScreen
from modules.suppliers import SuppliersScreen
from modules.transactions import TransactionsScreen
from modules.users import UsersScreen
from modules.reports import ReportsScreen
from modules.profile import ProfileScreen


class InventoryApp(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.title("Inventory Management System")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(900, 600)
        self.configure(bg=COLORS["bg_main"])

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() - WINDOW_WIDTH) // 2
        y = (self.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.geometry(f"+{x}+{y}")

        # Session state
        self.current_user = None
        self.active_nav = None
        self.nav_buttons = {}

        # Initialize DB
        initialize_database()

        # Container
        self.container = tk.Frame(self, bg=COLORS["bg_main"])
        self.container.pack(fill="both", expand=True)

        # Start with login
        self.show_login()

    # ════════════════════════════════════════
    #  Screen Navigation
    # ════════════════════════════════════════
    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login(self):
        self._clear_container()
        self.current_user = None
        LoginScreen(self.container, self).pack(fill="both", expand=True)

    def show_signup(self):
        self._clear_container()
        SignupScreen(self.container, self).pack(fill="both", expand=True)

    def show_main(self):
        """Build main layout with sidebar + content area."""
        self._clear_container()

        # ── Main layout ──
        main = tk.Frame(self.container, bg=COLORS["bg_main"])
        main.pack(fill="both", expand=True)

        # ── Sidebar ──
        self.sidebar = tk.Frame(main, bg=COLORS["bg_sidebar"],
                                 width=SIDEBAR_WIDTH)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self._build_sidebar()

        # ── Content area ──
        self.content_area = tk.Frame(main, bg=COLORS["bg_main"])
        self.content_area.pack(side="left", fill="both", expand=True)

        # ── Create all screens ──
        self.screens = {}
        self.screens["dashboard"] = DashboardScreen(self.content_area, self)
        self.screens["products"] = ProductsScreen(self.content_area, self)
        self.screens["categories"] = CategoriesScreen(self.content_area, self)
        self.screens["suppliers"] = SuppliersScreen(self.content_area, self)
        self.screens["transactions"] = TransactionsScreen(self.content_area, self)
        self.screens["reports"] = ReportsScreen(self.content_area, self)
        self.screens["profile"] = ProfileScreen(self.content_area, self)

        if self.current_user["role"] == "admin":
            self.screens["users"] = UsersScreen(self.content_area, self)

        # Show dashboard
        self._navigate("dashboard")

    def _build_sidebar(self):
        """Build the sidebar navigation."""
        # Logo area
        logo_frame = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"],
                               padx=16, pady=16)
        logo_frame.pack(fill="x")

        logo_icon = tk.Frame(logo_frame, bg=COLORS["primary"],
                              width=36, height=36)
        logo_icon.pack_propagate(False)
        logo_icon.pack(side="left", padx=(0, 10))
        tk.Label(logo_icon, text="IMS", font=("Segoe UI", 10, "bold"),
                 fg=COLORS["text_white"],
                 bg=COLORS["primary"]).place(relx=0.5, rely=0.5,
                                              anchor="center")

        tk.Label(logo_frame, text="Inventory MS",
                 font=FONTS["sidebar_bold"],
                 fg=COLORS["text_white"],
                 bg=COLORS["bg_sidebar"]).pack(side="left")

        # Separator
        tk.Frame(self.sidebar, bg="#334155", height=1).pack(fill="x",
                                                             padx=12,
                                                             pady=(0, 8))

        # Nav items
        nav_items = [
            ("dashboard", "📊  Dashboard"),
            ("products", "📦  Products"),
            ("categories", "🏷️  Categories"),
            ("suppliers", "🏭  Suppliers"),
            ("transactions", "🔄  Transactions"),
            ("reports", "📈  Reports"),
        ]

        # Admin-only
        if self.current_user["role"] == "admin":
            nav_items.append(("users", "👥  Users"))

        self.nav_buttons = {}
        for key, label in nav_items:
            btn = tk.Label(
                self.sidebar, text=label, font=FONTS["sidebar"],
                fg=COLORS["text_sidebar"], bg=COLORS["bg_sidebar"],
                anchor="w", padx=20, pady=10, cursor="hand2"
            )
            btn.pack(fill="x", padx=8, pady=1)
            btn.bind("<Button-1>", lambda e, k=key: self._navigate(k))
            btn.bind("<Enter>", lambda e, b=btn: self._nav_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self._nav_hover(b, False))
            self.nav_buttons[key] = btn

        # Spacer
        spacer = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"])
        spacer.pack(fill="both", expand=True)

        # Bottom section
        tk.Frame(self.sidebar, bg="#334155", height=1).pack(fill="x",
                                                             padx=12,
                                                             pady=(8, 0))

        # Profile button
        profile_btn = tk.Label(
            self.sidebar, text="⚙️  Settings", font=FONTS["sidebar"],
            fg=COLORS["text_sidebar"], bg=COLORS["bg_sidebar"],
            anchor="w", padx=20, pady=10, cursor="hand2"
        )
        profile_btn.pack(fill="x", padx=8, pady=1)
        profile_btn.bind("<Button-1>", lambda e: self._navigate("profile"))
        profile_btn.bind("<Enter>",
                         lambda e: self._nav_hover(profile_btn, True))
        profile_btn.bind("<Leave>",
                         lambda e: self._nav_hover(profile_btn, False))
        self.nav_buttons["profile"] = profile_btn

        # User info + logout
        user_frame = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"],
                               padx=16, pady=12)
        user_frame.pack(fill="x")

        initials = "".join(
            [w[0].upper()
             for w in self.current_user["full_name"].split()[:2]])

        avatar = tk.Frame(user_frame, bg="#7C3AED", width=32, height=32)
        avatar.pack_propagate(False)
        avatar.pack(side="left", padx=(0, 8))
        tk.Label(avatar, text=initials, font=("Segoe UI", 10, "bold"),
                 fg="white", bg="#7C3AED").place(relx=0.5, rely=0.5,
                                                  anchor="center")

        info = tk.Frame(user_frame, bg=COLORS["bg_sidebar"])
        info.pack(side="left", fill="x", expand=True)

        self.sidebar_name_label = tk.Label(
            info, text=self.current_user["full_name"],
            font=FONTS["small_bold"], fg=COLORS["text_white"],
            bg=COLORS["bg_sidebar"], anchor="w")
        self.sidebar_name_label.pack(fill="x")

        tk.Label(info, text=self.current_user["role"].title(),
                 font=FONTS["tiny"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_sidebar"], anchor="w").pack(fill="x")

        # Logout
        logout_btn = tk.Label(user_frame, text="🚪",
                               font=("Segoe UI", 14),
                               fg=COLORS["text_sidebar"],
                               bg=COLORS["bg_sidebar"],
                               cursor="hand2")
        logout_btn.pack(side="right")
        logout_btn.bind("<Button-1>", lambda e: self._logout())

    def _nav_hover(self, btn, entering):
        """Handle hover effects on nav buttons."""
        if btn.cget("bg") == COLORS["bg_sidebar_active"]:
            return  # Don't change active button
        if entering:
            btn.config(bg=COLORS["bg_sidebar_hover"])
        else:
            btn.config(bg=COLORS["bg_sidebar"])

    def _navigate(self, screen_key):
        """Switch to a screen."""
        # Update nav button styles
        for key, btn in self.nav_buttons.items():
            if key == screen_key:
                btn.config(bg=COLORS["bg_sidebar_active"],
                           fg=COLORS["text_white"])
            else:
                btn.config(bg=COLORS["bg_sidebar"],
                           fg=COLORS["text_sidebar"])

        # Hide all screens
        for screen in self.screens.values():
            screen.pack_forget()

        # Show target
        if screen_key in self.screens:
            self.screens[screen_key].pack(fill="both", expand=True)
            self.screens[screen_key].refresh()

        self.active_nav = screen_key

    def update_sidebar_user(self):
        """Update sidebar name label after profile edit."""
        if hasattr(self, "sidebar_name_label"):
            self.sidebar_name_label.config(
                text=self.current_user["full_name"])

    def _logout(self):
        self.current_user = None
        self.show_login()


# ════════════════════════════════════════
#  Entry Point
# ════════════════════════════════════════
if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
