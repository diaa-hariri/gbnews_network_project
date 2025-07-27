from flask import Blueprint, render_template, session, flash, redirect, url_for
from functools import wraps

it_backup_bp = Blueprint('it_backup', __name__, url_prefix='/it_backup')

def authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

@it_backup_bp.route('/')
@authenticated
def it_backup_index():
    return render_template(
        'sections/it-backup.html',
        user=session['user'],
    )
