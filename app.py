from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from functools import wraps
from datetime import datetime

from routes.users.login import login_user
from routes.users.register import register_user
from routes.pages.products import products_bp
from routes.pages.clients import clients_bp
from routes.pages.users import users_bp
from routes.pages.invoices import invoices_bp




app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(products_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(users_bp)
app.register_blueprint(invoices_bp)

CURR_DIR = os.path.dirname(__file__)

def authenticated(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        if 'user' not in session:
            flash('Veuillez vous connecter pour accéder au tableau de bord.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner_func

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_user(request)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_user(request, session)

@app.route('/dashboard')
@authenticated
def dashboard():
    return render_template(
        'dashboard.html',
        user=session['user'],
    )

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Déconnexion réussie!', 'success')
    return redirect(url_for('login'))

@app.context_processor
def inject_date_info():
    current_year = datetime.now().year
    full_current_date = datetime.now().strftime("%B %d, %Y")
    return {
        'current_year': current_year,
        'full_current_date': full_current_date
    }

if __name__ == '__main__':
    app.run(debug=True)
