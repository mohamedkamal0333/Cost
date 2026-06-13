# -*- coding: utf-8 -*-
"""
Database Manager - ادارة قاعدة البيانات SQLite
"""

import sqlite3
import os
from datetime import datetime, timedelta
from kivy.utils import platform

class DatabaseManager:
    """SQLite Database Manager for Customer Management"""

    def __init__(self):
        """Initialize database connection"""
        if platform == 'android':
            from android.storage import app_storage_path
            self.db_path = os.path.join(app_storage_path(), 'customer_manager.db')
        else:
            self.db_path = os.path.join(os.path.expanduser('~'), '.customer_manager', 'customer_manager.db')
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def init_database(self):
        """Initialize database tables"""
        conn, cursor = self.connect()

        # Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                service_type TEXT,
                amount REAL DEFAULT 0,
                paid_amount REAL DEFAULT 0,
                remaining_amount REAL DEFAULT 0,
                start_date TEXT,
                end_date TEXT,
                renewal_date TEXT,
                notes TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT DEFAULT 'cash',
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """)

        # Settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert default settings
        default_settings = [
            ('currency', 'ريال'),
            ('company_name', 'شركتي'),
            ('renewal_days', '7'),
            ('backup_enabled', '1'),
        ]

        for key, value in default_settings:
            cursor.execute("""
                INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)
            """, (key, value))

        conn.commit()
        self.close()

    # ========== CUSTOMER OPERATIONS ==========

    def add_customer(self, name, phone, email='', address='', service_type='',
                     amount=0, start_date='', end_date='', renewal_date='', notes=''):
        """Add new customer"""
        conn, cursor = self.connect()
        remaining = float(amount)

        cursor.execute("""
            INSERT INTO customers 
            (name, phone, email, address, service_type, amount, remaining_amount, 
             start_date, end_date, renewal_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, phone, email, address, service_type, amount, remaining,
              start_date, end_date, renewal_date, notes))

        customer_id = cursor.lastrowid
        conn.commit()
        self.close()
        return customer_id

    def update_customer(self, customer_id, **kwargs):
        """Update customer information"""
        conn, cursor = self.connect()

        allowed_fields = ['name', 'phone', 'email', 'address', 'service_type',
                         'amount', 'paid_amount', 'remaining_amount', 'start_date',
                         'end_date', 'renewal_date', 'notes', 'status']

        updates = []
        values = []
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = ?")
                values.append(value)

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(customer_id)

            query = f"UPDATE customers SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()

        self.close()
        return True

    def delete_customer(self, customer_id):
        """Delete customer and related payments"""
        conn, cursor = self.connect()
        cursor.execute('DELETE FROM payments WHERE customer_id = ?', (customer_id,))
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()
        self.close()
        return True

    def get_customer(self, customer_id):
        """Get single customer by ID"""
        conn, cursor = self.connect()
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        row = cursor.fetchone()
        self.close()
        return dict(row) if row else None

    def get_all_customers(self, status=None):
        """Get all customers with optional status filter"""
        conn, cursor = self.connect()

        if status:
            cursor.execute('SELECT * FROM customers WHERE status = ? ORDER BY name', (status,))
        else:
            cursor.execute('SELECT * FROM customers ORDER BY name')

        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def search_customers(self, query):
        """Search customers by name or phone"""
        conn, cursor = self.connect()
        search_term = f'%{query}%'
        cursor.execute("""
            SELECT * FROM customers 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
            ORDER BY name
        """, (search_term, search_term, search_term))
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    # ========== PAYMENT OPERATIONS ==========

    def add_payment(self, customer_id, amount, payment_method='cash', notes=''):
        """Add payment for customer"""
        conn, cursor = self.connect()

        cursor.execute("""
            INSERT INTO payments (customer_id, amount, payment_method, notes)
            VALUES (?, ?, ?, ?)
        """, (customer_id, amount, payment_method, notes))

        cursor.execute("""
            UPDATE customers 
            SET paid_amount = paid_amount + ?,
                remaining_amount = amount - (paid_amount + ?),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (amount, amount, customer_id))

        conn.commit()
        self.close()
        return True

    def get_customer_payments(self, customer_id):
        """Get all payments for a customer"""
        conn, cursor = self.connect()
        cursor.execute("""
            SELECT * FROM payments WHERE customer_id = ? ORDER BY payment_date DESC
        """, (customer_id,))
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def get_all_payments(self):
        """Get all payments"""
        conn, cursor = self.connect()
        cursor.execute("""
            SELECT p.*, c.name as customer_name 
            FROM payments p
            JOIN customers c ON p.customer_id = c.id
            ORDER BY p.payment_date DESC
        """)
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    # ========== REPORTS & STATISTICS ==========

    def get_statistics(self):
        """Get dashboard statistics"""
        conn, cursor = self.connect()

        cursor.execute('SELECT COUNT(*) as total FROM customers')
        total_customers = cursor.fetchone()['total']

        cursor.execute('SELECT COALESCE(SUM(amount), 0) as total FROM customers')
        total_amount = cursor.fetchone()['total']

        cursor.execute('SELECT COALESCE(SUM(paid_amount), 0) as total FROM customers')
        total_paid = cursor.fetchone()['total']

        remaining = total_amount - total_paid

        cursor.execute("SELECT COUNT(*) as total FROM customers WHERE status = 'active'")
        active = cursor.fetchone()['total']

        self.close()

        return {
            'total_customers': total_customers,
            'total_amount': total_amount,
            'total_paid': total_paid,
            'total_remaining': remaining,
            'active_customers': active
        }

    def get_upcoming_renewals(self, days=7):
        """Get customers with upcoming renewals"""
        conn, cursor = self.connect()
        today = datetime.now().strftime('%Y-%m-%d')
        future = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

        cursor.execute("""
            SELECT * FROM customers 
            WHERE renewal_date BETWEEN ? AND ?
            AND status = 'active'
            ORDER BY renewal_date
        """, (today, future))

        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def get_overdue_customers(self):
        """Get customers with overdue payments"""
        conn, cursor = self.connect()
        today = datetime.now().strftime('%Y-%m-%d')

        cursor.execute("""
            SELECT * FROM customers 
            WHERE remaining_amount > 0 
            AND end_date < ?
            AND status = 'active'
            ORDER BY end_date
        """, (today,))

        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    # ========== SETTINGS ==========

    def get_setting(self, key, default=None):
        """Get setting value"""
        conn, cursor = self.connect()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        self.close()
        return row['value'] if row else default

    def set_setting(self, key, value):
        """Set setting value"""
        conn, cursor = self.connect()
        cursor.execute("""
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
        """, (key, value))
        conn.commit()
        self.close()
        return True

    # ========== EXPORT ==========

    def get_all_data_for_export(self):
        """Get all data for export"""
        conn, cursor = self.connect()

        cursor.execute('SELECT * FROM customers ORDER BY id')
        customers = [dict(row) for row in cursor.fetchall()]

        cursor.execute('SELECT * FROM payments ORDER BY id')
        payments = [dict(row) for row in cursor.fetchall()]

        self.close()
        return {'customers': customers, 'payments': payments}
