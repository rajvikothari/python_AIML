"""
Custom reusable widgets for the Inventory Management System.
Provides styled buttons, inputs, cards, stat cards, and table widgets.
"""

import tkinter as tk
from tkinter import ttk
from theme import COLORS, FONTS, CARD_RADIUS, INPUT_RADIUS, BUTTON_RADIUS


# ══════════════════════════════════════════════
#  Rounded Frame (Card)
# ══════════════════════════════════════════════
class CardFrame(tk.Frame):
    """A frame styled as a card with white background."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["bg_card"],
                         highlightbackground=COLORS["border"],
                         highlightthickness=1, **kwargs)


# ══════════════════════════════════════════════
#  Styled Button
# ══════════════════════════════════════════════
class StyledButton(tk.Canvas):
    """A flat styled button with hover effects."""

    def __init__(self, parent, text="Button", command=None,
                 bg=None, fg=None, width=120, height=36,
                 font=None, **kwargs):
        self.bg_color = bg or COLORS["primary"]
        self.fg_color = fg or COLORS["text_white"]
        self.hover_color = self._darken(self.bg_color)
        self.command = command
        self.btn_width = width
        self.btn_height = height

        super().__init__(parent, width=width, height=height,
                         bg=parent.cget("bg"), highlightthickness=0,
                         **kwargs)

        self._draw(self.bg_color)
        self.create_text(width // 2, height // 2, text=text,
                         fill=self.fg_color,
                         font=font or FONTS["button"],
                         tags="text")

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _draw(self, color):
        self.delete("bg")
        r = BUTTON_RADIUS
        w, h = self.btn_width, self.btn_height
        self.create_round_rect(2, 2, w - 2, h - 2, r, fill=color,
                               outline="", tags="bg")
        self.tag_lower("bg")

    def create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _darken(self, hex_color):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        factor = 0.85
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _on_enter(self, event):
        self._draw(self.hover_color)

    def _on_leave(self, event):
        self._draw(self.bg_color)

    def _on_click(self, event):
        if self.command:
            self.command()


# ══════════════════════════════════════════════
#  Styled Entry (Input Field)
# ══════════════════════════════════════════════
class StyledEntry(tk.Frame):
    """A styled input field with label and placeholder."""

    def __init__(self, parent, label="", placeholder="", show="",
                 width=280, **kwargs):
        super().__init__(parent, bg=parent.cget("bg"), **kwargs)

        if label:
            lbl = tk.Label(self, text=label, font=FONTS["small_bold"],
                           fg=COLORS["text_secondary"], bg=self.cget("bg"))
            lbl.pack(anchor="w", pady=(0, 4))

        self.entry_var = tk.StringVar()
        entry_frame = tk.Frame(self, bg=COLORS["border"],
                               highlightthickness=0)
        entry_frame.pack(fill="x")

        inner = tk.Frame(entry_frame, bg=COLORS["bg_input"], padx=1, pady=1)
        inner.pack(fill="x", padx=1, pady=1)

        self.entry = tk.Entry(inner, textvariable=self.entry_var,
                              font=FONTS["input"], bg=COLORS["bg_input"],
                              fg=COLORS["text_primary"],
                              insertbackground=COLORS["text_primary"],
                              relief="flat", width=width // 8,
                              show=show if show else "")
        self.entry.pack(fill="x", ipady=8, padx=8)

        if placeholder:
            self._placeholder = placeholder
            self._is_placeholder = True
            self.entry.insert(0, placeholder)
            self.entry.config(fg=COLORS["text_muted"])
            self.entry.bind("<FocusIn>", self._clear_placeholder)
            self.entry.bind("<FocusOut>", self._set_placeholder)

    def _clear_placeholder(self, event):
        if self._is_placeholder:
            self.entry.delete(0, "end")
            self.entry.config(fg=COLORS["text_primary"])
            self._is_placeholder = False

    def _set_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, self._placeholder)
            self.entry.config(fg=COLORS["text_muted"])
            self._is_placeholder = True

    def get(self):
        if hasattr(self, "_is_placeholder") and self._is_placeholder:
            return ""
        return self.entry_var.get()

    def set(self, value):
        if hasattr(self, "_is_placeholder"):
            self._is_placeholder = False
            self.entry.config(fg=COLORS["text_primary"])
        self.entry_var.set(value)

    def clear(self):
        self.entry_var.set("")
        if hasattr(self, "_placeholder"):
            self._is_placeholder = True
            self.entry.insert(0, self._placeholder)
            self.entry.config(fg=COLORS["text_muted"])


# ══════════════════════════════════════════════
#  Stat Card
# ══════════════════════════════════════════════
class StatCard(tk.Frame):
    """Dashboard stat card with icon, value, and label."""

    def __init__(self, parent, label="", value="0", icon="📦",
                 accent_color=None, **kwargs):
        accent = accent_color or COLORS["primary"]
        super().__init__(parent, bg=COLORS["bg_card"],
                         highlightbackground=COLORS["border"],
                         highlightthickness=1, **kwargs)

        inner = tk.Frame(self, bg=COLORS["bg_card"], padx=16, pady=14)
        inner.pack(fill="both", expand=True)

        top = tk.Frame(inner, bg=COLORS["bg_card"])
        top.pack(fill="x")

        icon_lbl = tk.Label(top, text=icon, font=("Segoe UI", 18),
                            bg=COLORS["bg_card"])
        icon_lbl.pack(side="left")

        val_lbl = tk.Label(inner, text=str(value),
                           font=FONTS["stat_number"],
                           fg=accent, bg=COLORS["bg_card"])
        val_lbl.pack(anchor="w", pady=(8, 2))
        self.value_label = val_lbl

        txt_lbl = tk.Label(inner, text=label, font=FONTS["stat_label"],
                           fg=COLORS["text_secondary"], bg=COLORS["bg_card"])
        txt_lbl.pack(anchor="w")

    def update_value(self, new_value):
        self.value_label.config(text=str(new_value))


# ══════════════════════════════════════════════
#  Data Table (Treeview wrapper)
# ══════════════════════════════════════════════
class DataTable(tk.Frame):
    """Styled Treeview table with scrollbar."""

    def __init__(self, parent, columns, column_widths=None,
                 row_height=32, **kwargs):
        super().__init__(parent, bg=COLORS["bg_card"], **kwargs)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Custom.Treeview",
                        background=COLORS["bg_card"],
                        foreground=COLORS["text_primary"],
                        fieldbackground=COLORS["bg_card"],
                        font=FONTS["body"],
                        rowheight=row_height,
                        borderwidth=0)

        style.configure("Custom.Treeview.Heading",
                        background=COLORS["bg_main"],
                        foreground=COLORS["text_secondary"],
                        font=FONTS["small_bold"],
                        borderwidth=0,
                        relief="flat")

        style.map("Custom.Treeview",
                  background=[("selected", COLORS["primary_light"])],
                  foreground=[("selected", COLORS["primary"])])

        style.map("Custom.Treeview.Heading",
                  background=[("active", COLORS["bg_main"])])

        # Treeview
        self.tree = ttk.Treeview(self, columns=columns,
                                 show="headings",
                                 style="Custom.Treeview",
                                 selectmode="browse")

        for i, col in enumerate(columns):
            w = column_widths[i] if column_widths and i < len(column_widths) else 120
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, minwidth=50, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self, rows):
        """Clear and reload all rows."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert("", "end", values=row)

    def get_selected(self):
        """Return the values of the selected row."""
        sel = self.tree.selection()
        if sel:
            return self.tree.item(sel[0])["values"]
        return None

    def bind_select(self, callback):
        self.tree.bind("<<TreeviewSelect>>", callback)


# ══════════════════════════════════════════════
#  Search Bar
# ══════════════════════════════════════════════
class SearchBar(tk.Frame):
    """Search input with icon styling."""

    def __init__(self, parent, placeholder="Search...",
                 on_search=None, **kwargs):
        super().__init__(parent, bg=parent.cget("bg"), **kwargs)

        self.on_search = on_search

        container = tk.Frame(self, bg=COLORS["border"])
        container.pack(fill="x")

        inner = tk.Frame(container, bg=COLORS["bg_input"])
        inner.pack(fill="x", padx=1, pady=1)

        icon = tk.Label(inner, text="🔍", font=("Segoe UI", 11),
                        bg=COLORS["bg_input"])
        icon.pack(side="left", padx=(8, 4))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_change)

        self.entry = tk.Entry(inner, textvariable=self.search_var,
                              font=FONTS["input"], bg=COLORS["bg_input"],
                              fg=COLORS["text_primary"],
                              insertbackground=COLORS["text_primary"],
                              relief="flat", width=30)
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=4)

        # Placeholder
        self._placeholder = placeholder
        self._is_placeholder = True
        self.entry.insert(0, placeholder)
        self.entry.config(fg=COLORS["text_muted"])
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._set_placeholder)

    def _clear_placeholder(self, event):
        if self._is_placeholder:
            self.entry.delete(0, "end")
            self.entry.config(fg=COLORS["text_primary"])
            self._is_placeholder = False

    def _set_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, self._placeholder)
            self.entry.config(fg=COLORS["text_muted"])
            self._is_placeholder = True

    def _on_change(self, *args):
        if self.on_search and not self._is_placeholder:
            self.on_search(self.search_var.get())

    def get(self):
        if self._is_placeholder:
            return ""
        return self.search_var.get()
