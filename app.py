from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from functools import wraps
from datetime import datetime
import json

from routes.users.login import login_user
from routes.users.register import register_user
from routes.pages.inventory import inventory_bp
from routes.pages.it_production import it_production_bp
from routes.pages.it_development import it_development_bp
from routes.pages.it_backup import it_backup_bp
from routes.pages import it_continuity_bp
from routes.pages.it_improvement import it_improvement_bp
from routes.pages.it_decision import it_decision_bp


app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(inventory_bp)
app.register_blueprint(it_production_bp)
app.register_blueprint(it_development_bp)
app.register_blueprint(it_backup_bp)
app.register_blueprint(it_continuity_bp)
app.register_blueprint(it_improvement_bp)
app.register_blueprint(it_decision_bp)

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
