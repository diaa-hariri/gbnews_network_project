from flask import Blueprint, render_template, session, flash, redirect, url_for
from functools import wraps

it_decision_bp = Blueprint('it_decision', __name__, url_prefix='/it_decision')

def authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

@it_decision_bp.route('/')
@authenticated
def it_decision_index():
    return render_template(
        'sections/it-decision.html',
        user=session['user'],
    )
