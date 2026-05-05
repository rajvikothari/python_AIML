"""
Database module for Inventory Management System.
Handles SQLite connection, table creation, and seed data.
"""

import sqlite3
import hashlib
import os

DB_NAME = "inventory.db"


def get_connection():
    """Get a database connection with row_factory enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with a fixed salt."""
    salt = "ims_secure_salt_2025"
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def initialize_database():
    """Create all tables and seed default data."""
    conn = get_connection()
    cursor = conn.cursor()

    # ── Users table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL DEFAULT 'staff',
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── Categories table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT '#534AB7',
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── Suppliers table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── Products table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT UNIQUE NOT NULL,
            category_id INTEGER,
            supplier_id INTEGER,
            price REAL DEFAULT 0.0,
            quantity INTEGER DEFAULT 0,
            reorder_level INTEGER DEFAULT 10,
            location TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
        )
    """)

    # ── Stock Transactions table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # ── Seed default admin ──
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (username, password, full_name, email, role, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("admin", hash_password("admin123"), "System Admin",
              "admin@ims.com", "admin", "active"))

    # ── Seed default staff ──
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'staff'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (username, password, full_name, email, role, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("staff", hash_password("staff123"), "John Staff",
              "staff@ims.com", "staff", "active"))

    # ── Seed categories ──
    default_categories = [
        ("Electronics", "#534AB7", "Electronic devices and components"),
        ("Accessories", "#1D9E75", "Device accessories and peripherals"),
        ("Furniture", "#D85A30", "Office and home furniture"),
        ("Stationery", "#185FA5", "Office supplies and stationery"),
        ("Clothing", "#D4537E", "Apparel and wearable items"),
    ]
    for name, color, desc in default_categories:
        cursor.execute("SELECT COUNT(*) FROM categories WHERE name = ?", (name,))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO categories (name, color, description) VALUES (?, ?, ?)",
                (name, color, desc))

    # ── Seed suppliers ──
    default_suppliers = [
        ("TechWorld Supplies", "Alice Chen", "+1-555-0101", "alice@techworld.com", "123 Tech Lane, CA"),
        ("OfficeMax Direct", "Bob Martin", "+1-555-0202", "bob@officemax.com", "456 Office Blvd, NY"),
        ("Global Furnish Co", "Carol White", "+1-555-0303", "carol@globalfurnish.com", "789 Furnish St, TX"),
    ]
    for name, cp, phone, email, addr in default_suppliers:
        cursor.execute("SELECT COUNT(*) FROM suppliers WHERE name = ?", (name,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO suppliers (name, contact_person, phone, email, address)
                VALUES (?, ?, ?, ?, ?)
            """, (name, cp, phone, email, addr))

    # ── Seed products ──
    default_products = [
        ("Wireless Mouse", "WM-1042", 1, 1, 24.99, 342, 20, "Shelf A1"),
        ("USB-C Cable", "UC-0387", 2, 1, 9.99, 8, 15, "Shelf B2"),
        ("Bluetooth Speaker", "BS-2201", 1, 1, 49.99, 127, 10, "Shelf A3"),
        ("Office Chair", "OC-1100", 3, 3, 189.99, 35, 5, "Warehouse C"),
        ("Notebook Pack", "NP-0050", 4, 2, 12.50, 500, 50, "Shelf D1"),
        ("LED Monitor 24in", "LM-2400", 1, 1, 199.99, 64, 10, "Shelf A2"),
        ("Keyboard Mechanical", "KM-0770", 1, 1, 79.99, 98, 15, "Shelf A4"),
        ("Desk Lamp", "DL-0330", 3, 3, 34.99, 3, 10, "Shelf C1"),
        ("Printer Paper A4", "PP-0010", 4, 2, 8.99, 1200, 100, "Shelf D2"),
        ("Polo T-Shirt", "PT-0500", 5, 2, 29.99, 75, 20, "Shelf E1"),
    ]
    for name, sku, cat, sup, price, qty, reorder, loc in default_products:
        cursor.execute("SELECT COUNT(*) FROM products WHERE sku = ?", (sku,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO products (name, sku, category_id, supplier_id, price, quantity, reorder_level, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, sku, cat, sup, price, qty, reorder, loc))

    # ── Seed some transactions ──
    cursor.execute("SELECT COUNT(*) FROM transactions")
    if cursor.fetchone()[0] == 0:
        sample_txns = [
            (1, 1, "in", 50, "Restocked from TechWorld"),
            (2, 1, "out", 12, "Shipped to client order #1023"),
            (3, 1, "in", 30, "New batch arrival"),
            (5, 2, "out", 25, "Office supplies distribution"),
            (6, 1, "in", 10, "Replacement units"),
            (8, 1, "out", 7, "Employee requests"),
        ]
        for pid, uid, typ, qty, notes in sample_txns:
            cursor.execute("""
                INSERT INTO transactions (product_id, user_id, type, quantity, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (pid, uid, typ, qty, notes))

    conn.commit()
    conn.close()
