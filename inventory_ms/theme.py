"""
Theme configuration for the Inventory Management System.
Modern flat card-based design with consistent colors and fonts.
"""

# ── Color Palette ──
COLORS = {
    # Primary
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "primary_light": "#DBEAFE",
    "primary_dark": "#1E3A5F",

    # Backgrounds
    "bg_main": "#F1F5F9",
    "bg_card": "#FFFFFF",
    "bg_sidebar": "#1E293B",
    "bg_sidebar_hover": "#334155",
    "bg_sidebar_active": "#2563EB",
    "bg_input": "#F8FAFC",

    # Text
    "text_primary": "#0F172A",
    "text_secondary": "#64748B",
    "text_muted": "#94A3B8",
    "text_white": "#FFFFFF",
    "text_sidebar": "#CBD5E1",

    # Status
    "success": "#16A34A",
    "success_bg": "#DCFCE7",
    "warning": "#D97706",
    "warning_bg": "#FEF3C7",
    "danger": "#DC2626",
    "danger_bg": "#FEE2E2",
    "info": "#2563EB",
    "info_bg": "#DBEAFE",

    # Borders
    "border": "#E2E8F0",
    "border_focus": "#2563EB",

    # Category colors
    "cat_purple": "#7C3AED",
    "cat_purple_bg": "#EDE9FE",
    "cat_teal": "#0D9488",
    "cat_teal_bg": "#CCFBF1",
    "cat_coral": "#EA580C",
    "cat_coral_bg": "#FFF7ED",
    "cat_blue": "#2563EB",
    "cat_blue_bg": "#DBEAFE",
    "cat_pink": "#DB2777",
    "cat_pink_bg": "#FCE7F3",
}

# ── Category color map ──
CATEGORY_COLORS = [
    ("#7C3AED", "#EDE9FE"),  # Purple
    ("#0D9488", "#CCFBF1"),  # Teal
    ("#EA580C", "#FFF7ED"),  # Coral
    ("#2563EB", "#DBEAFE"),  # Blue
    ("#DB2777", "#FCE7F3"),  # Pink
    ("#CA8A04", "#FEF9C3"),  # Amber
    ("#059669", "#D1FAE5"),  # Emerald
    ("#DC2626", "#FEE2E2"),  # Red
]

# ── Font Sizes ──
FONTS = {
    "heading_xl": ("Segoe UI", 22, "bold"),
    "heading_lg": ("Segoe UI", 18, "bold"),
    "heading_md": ("Segoe UI", 15, "bold"),
    "body": ("Segoe UI", 13),
    "body_bold": ("Segoe UI", 13, "bold"),
    "small": ("Segoe UI", 11),
    "small_bold": ("Segoe UI", 11, "bold"),
    "tiny": ("Segoe UI", 10),
    "sidebar": ("Segoe UI", 13),
    "sidebar_bold": ("Segoe UI", 13, "bold"),
    "button": ("Segoe UI", 12, "bold"),
    "input": ("Segoe UI", 12),
    "stat_number": ("Segoe UI", 26, "bold"),
    "stat_label": ("Segoe UI", 11),
}

# ── Dimensions ──
SIDEBAR_WIDTH = 220
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
CARD_RADIUS = 12
INPUT_RADIUS = 8
BUTTON_RADIUS = 8
PADDING = 16
