# 🏭 Inventory Management System

A full-featured Inventory Management System built with Python & Tkinter, featuring role-based authentication, product/category/supplier management, stock transactions, reports with charts, and a modern flat card-based UI.

---

## 📂 Project Structure

```
inventory_ms/
├── main.py              ← Entry point (run this)
├── database.py          ← SQLite DB setup, tables, seed data
├── theme.py             ← Colors, fonts, dimensions
├── widgets.py           ← Reusable UI components
├── modules/
│   ├── __init__.py
│   ├── auth.py          ← Login & Signup screens
│   ├── dashboard.py     ← Dashboard with stat cards
│   ├── products.py      ← Product CRUD
│   ├── categories.py    ← Category CRUD
│   ├── suppliers.py     ← Supplier CRUD
│   ├── transactions.py  ← Stock In / Stock Out
│   ├── users.py         ← User management (admin)
│   ├── reports.py       ← Reports & charts
│   └── profile.py       ← Profile & settings
└── inventory.db         ← Auto-created on first run
```

---

## 🚀 Setup & Run

### Prerequisites
- **Python 3.8+** (tkinter is included with Python on most systems)

### Steps

1. **Download / Copy** the entire `inventory_ms` folder to your laptop.

2. **Install matplotlib** (optional, for charts in Reports):
   ```bash
   pip install matplotlib
   ```
   > The app works without matplotlib — reports will show text-based summaries instead of charts.

3. **Run the app**:
   ```bash
   cd inventory_ms
   python main.py
   ```

4. **Login** with default credentials:
   | Role  | Username | Password  |
   |-------|----------|-----------|
   | Admin | admin    | admin123  |
   | Staff | staff    | staff123  |

---

## 🔐 Roles & Permissions

| Feature              | Admin | Staff |
|----------------------|-------|-------|
| Dashboard            | ✅    | ✅    |
| View Products        | ✅    | ✅    |
| Add/Edit/Delete Products | ✅ | ✅   |
| Manage Categories    | ✅    | ✅    |
| Manage Suppliers     | ✅    | ✅    |
| Stock In / Out       | ✅    | ✅    |
| Reports & Charts     | ✅    | ✅    |
| User Management      | ✅    | ❌    |
| Approve New Users    | ✅    | ❌    |

---

## ✨ Features

- **Authentication** — Login, Signup with pending approval, password hashing (SHA-256)
- **Dashboard** — Live stat cards, recent activity feed
- **Product Management** — Full CRUD with search & category filter
- **Category Management** — Color-coded categories with product count
- **Supplier Management** — Contact info, linked product count
- **Stock Transactions** — Stock in/out with validation, auto quantity update
- **User Management** — Approve, toggle roles, deactivate, delete users
- **Reports** — Low stock alerts, category pie chart, supplier breakdown, activity bar chart
- **Profile** — Edit name/email, change password
- **Modern UI** — Flat card-based design, sidebar navigation, hover effects

---

## 🛠 Tech Stack

| Component  | Technology        |
|-----------|-------------------|
| Language  | Python 3          |
| GUI       | tkinter + ttk     |
| Database  | SQLite3           |
| Charts    | matplotlib (optional) |
| Security  | hashlib SHA-256   |

---

## 📝 Notes

- The SQLite database (`inventory.db`) is auto-created with seed data on first run.
- Delete `inventory.db` to reset all data back to defaults.
- The app window is resizable with a minimum size of 900×600.
