import sqlite3

def init_db():
    conn = sqlite3.connect('data/alnormarket.db')
    cursor = conn.cursor()

    # Create clients table (already English)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            full_address TEXT,
            phone_number TEXT,
            logo_filename TEXT,
            added_by TEXT,
            added_date TEXT
        )
    ''')

    # Create products table (also need to rename columns to English)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            product_description TEXT,
            product_price REAL,
            image_filename TEXT,
            quantity_type TEXT,
            number_of_cartons INTEGER,
            pieces_per_carton INTEGER,
            total_pieces INTEGER,
            date_added TEXT,
            added_by TEXT
        )
    ''')

    # Create factures table (invoices) with English column names
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            invoice_date TEXT,
            invoice_number TEXT UNIQUE,
            added_by TEXT,
            total_amount REAL
        )
    ''')

    # Create invoice_items table with English column names
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            unit_price REAL,
            line_total REAL,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id)
        )
    ''')

    # Create users table (already English)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
