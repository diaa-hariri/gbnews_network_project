import sys
import os

# أضف المجلد الجذري للمشروع إلى sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from flask import Blueprint, render_template, session, flash, redirect, url_for
from functools import wraps
from data.database import get_db_connection  # استيراد مباشر بعد تعديل sys.path

users_bp = Blueprint('users', __name__, url_prefix='/users')

def authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

@users_bp.route('/', methods=['GET'])
@authenticated
def users_index():
    conn = get_db_connection()
    try:
        users = conn.execute("SELECT * FROM users ORDER BY username ASC").fetchall()
    except Exception as e:
        users = []
        flash(f"Erreur lors de la récupération des utilisateurs: {e}", "danger")
    finally:
        conn.close()
    return render_template('users.html', users=users, user=session['user'])
