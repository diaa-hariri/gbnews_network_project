import os
from datetime import datetime
from flask import Blueprint, render_template, session, flash, redirect, url_for, request, current_app
from functools import wraps
from werkzeug.utils import secure_filename
from data.database import get_db_connection  # Make sure this exists and works

products_bp = Blueprint('products', __name__, url_prefix='/products')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

@products_bp.route('/', methods=['GET', 'POST'])
@authenticated
def products_index():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        product_name = request.form.get('product_name')
        product_description = request.form.get('product_description')
        product_price = float(request.form.get('product_price'))
        quantity_type = request.form.get('quantity_type')
        quantity_value = int(request.form.get('quantity_in_stock'))
        pieces_per_carton = request.form.get('pieces_per_carton')

        user = session['user'].get('displayName') or session['user'].get('username') or 'Utilisateur inconnu'
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        image_file = request.files.get('image_file')
        image_filename = None

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            images_path = os.path.join(current_app.root_path, 'static', 'images', 'products')
            os.makedirs(images_path, exist_ok=True)
            filepath = os.path.join(images_path, filename)
            image_file.save(filepath)
            image_filename = filename
        else:
            flash('Fichier image invalide ou manquant.', 'danger')
            return redirect(url_for('products.products_index'))

        total_pieces = quantity_value
        number_of_cartons = None
        pieces_per_carton = int(pieces_per_carton) if pieces_per_carton else None

        if quantity_type == 'cartons':
            number_of_cartons = quantity_value
            total_pieces = number_of_cartons * (pieces_per_carton or 1)

        cursor.execute('''
            INSERT INTO products (
                product_name, product_description, product_price,
                image_filename, quantity_type, number_of_cartons,
                pieces_per_carton, total_pieces, date_added, added_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product_name, product_description, product_price,
            image_filename, quantity_type, number_of_cartons,
            pieces_per_carton, total_pieces, date_added, user
        ))

        conn.commit()
        conn.close()

        flash('Produit ajouté avec succès!', 'success')
        return redirect(url_for('products.products_index'))

    cursor.execute('SELECT * FROM products ORDER BY date_added DESC')
    products = cursor.fetchall()
    conn.close()

    return render_template('sections/products.html', user=session['user'], products=products)
