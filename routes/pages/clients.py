import os
import sys
import uuid
from datetime import datetime
from flask import Blueprint, render_template, session, flash, redirect, url_for, request, current_app
from functools import wraps
from werkzeug.utils import secure_filename

# أضف جذر المشروع إلى sys.path لاستيراد database.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from data.database import get_db_connection


clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

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

def dict_factory(cursor, row):
    """Helper to convert DB rows to dictionaries."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@clients_bp.route('/', methods=['GET', 'POST'])
@authenticated
def clients_index():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.row_factory = dict_factory

        name = request.form.get('name')
        description = request.form.get('description')
        address = request.form.get('address')
        phone = request.form.get('phone')

        # Logo upload
        logo_file = request.files.get('logo')
        logo_filename = None
        if logo_file and allowed_file(logo_file.filename):
            logo_filename = secure_filename(f"{uuid.uuid4()}_{logo_file.filename}")
            logo_path = os.path.join(current_app.root_path, 'static', 'images', 'logos')
            os.makedirs(logo_path, exist_ok=True)
            logo_file.save(os.path.join(logo_path, logo_filename))

        new_client = {
            "name": name,
            "description": description,
            "full_address": address,
            "phone_number": phone,
            "logo_filename": logo_filename,
            "added_by": session['user'].get('displayName') or session['user'].get('username') or "unknown",
            "added_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            conn.execute(
                """
                INSERT INTO clients
                (name, description, full_address, phone_number, logo_filename, added_by, added_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    new_client['name'],
                    new_client['description'],
                    new_client['full_address'],
                    new_client['phone_number'],
                    new_client['logo_filename'],
                    new_client['added_by'],
                    new_client['added_date']
                )
            )
            conn.commit()
            flash("Client ajouté avec succès.", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Erreur lors de l'ajout du client: {e}", "danger")
        finally:
            conn.close()

        return redirect(url_for('clients.clients_index'))

    # GET method
    conn = get_db_connection()
    conn.row_factory = dict_factory

    try:
        clients = conn.execute("SELECT * FROM clients ORDER BY added_date DESC").fetchall()
    except Exception as e:
        clients = []
        flash(f"Erreur lors de la récupération des clients: {e}", "danger")
    finally:
        conn.close()

    return render_template('sections/clients.html', user=session['user'], clients=clients)
