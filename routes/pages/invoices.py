from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from data.database import get_db_connection
from functools import wraps
from datetime import datetime

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

def authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

@invoices_bp.route('/')
@authenticated
def invoices_list():
    conn = get_db_connection()
    invoices = conn.execute("SELECT * FROM invoices ORDER BY invoice_date DESC").fetchall()
    conn.close()
    return render_template('sections/invoices.html', invoices=invoices, user=session['user'])

@invoices_bp.route('/<int:invoice_id>')
@authenticated
def invoice_detail(invoice_id):
    conn = get_db_connection()
    invoice = conn.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,)).fetchone()
    items = conn.execute("SELECT * FROM invoice_items WHERE invoice_id = ?", (invoice_id,)).fetchall()
    conn.close()

    if not invoice:
        flash("Invoice not found.", "danger")
        return redirect(url_for('invoices.invoices_list'))

    return render_template('sections/invoice_detail.html', invoice=invoice, items=items, user=session['user'])

@invoices_bp.route('/add', methods=['GET', 'POST'])
@authenticated
def add_invoice():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        client_id = request.form['client_id']
        invoice_number = request.form['invoice_number']
        invoice_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        added_by = session['user'].get('displayName') or session['user'].get('username') or "unknown"

        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        unit_prices = request.form.getlist('unit_price[]')

        total_invoice = 0
        items = []

        try:
            for prod_id, qty, input_price in zip(product_ids, quantities, unit_prices):
                qty = int(qty)

                # جلب السعر الحقيقي من قاعدة البيانات
                prod_row = cursor.execute("SELECT product_name, product_price FROM products WHERE id = ?", (prod_id,)).fetchone()

                if not prod_row:
                    raise ValueError("Invalid product ID")

                product_name = prod_row['product_name']
                unit_price = float(prod_row['product_price'])

                line_total = qty * unit_price
                total_invoice += line_total

                items.append((product_name, qty, unit_price, line_total))
        except ValueError:
            flash("Please enter valid quantities and select valid products.", "danger")
            clients = cursor.execute("SELECT id, name FROM clients").fetchall()
            products = cursor.execute("SELECT id, product_name, product_price FROM products").fetchall()
            conn.close()
            return render_template('sections/add_invoice.html', user=session['user'], clients=clients, products=products)

        try:
            client_row = cursor.execute("SELECT name FROM clients WHERE id = ?", (client_id,)).fetchone()
            if not client_row:
                flash("Selected client does not exist.", "danger")
                clients = cursor.execute("SELECT id, name FROM clients").fetchall()
                products = cursor.execute("SELECT id, product_name, product_price FROM products").fetchall()
                conn.close()
                return render_template('sections/add_invoice.html', user=session['user'], clients=clients, products=products)

            client_name = client_row['name']

            # حفظ الفاتورة
            cursor.execute('''
                INSERT INTO invoices (client_name, invoice_date, invoice_number, added_by, total_amount)
                VALUES (?, ?, ?, ?, ?)
            ''', (client_name, invoice_date, invoice_number, added_by, total_invoice))
            invoice_id = cursor.lastrowid

            # حفظ العناصر
            for item in items:
                cursor.execute('''
                    INSERT INTO invoice_items (invoice_id, product_name, quantity, unit_price, line_total)
                    VALUES (?, ?, ?, ?, ?)
                ''', (invoice_id, *item))

            conn.commit()
            flash("✅ Invoice added successfully.", "success")
            return redirect(url_for('invoices.invoices_list'))

        except Exception as e:
            conn.rollback()
            flash(f"❌ Error adding invoice: {e}", "danger")
        finally:
            conn.close()

    # GET Request
    clients = cursor.execute("SELECT id, name FROM clients").fetchall()
    products = cursor.execute("SELECT id, product_name, product_price FROM products").fetchall()
    conn.close()
    return render_template('sections/add_invoice.html', user=session['user'], clients=clients, products=products)
