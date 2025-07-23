from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from functools import wraps
from datetime import datetime
import json

from config.firestore_db import db
from routes.users.login import login_user
from routes.users.register import register_user


app = Flask(__name__)
app.secret_key = os.urandom(24)

CURR_DIR = os.path.dirname(__file__)

def authenticated(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner_func

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_user(request)

@app.route('/it_production')
@authenticated
def it_production_index():
    return render_template(
        'it-production.html',
        user=session['user'],
    )

@app.route('/it_production/inventory')
@authenticated
def it_production_inventory():
    json_path = os.path.join(CURR_DIR, 'data/database.json')

    devices = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    devices = data.get("Inventory", [])
            except json.JSONDecodeError:
                flash("Erreur de format dans le fichier JSON des appareils.", "danger")

    return render_template(
        'it-production.html',
        user=session['user'],
        active_tab='inventory',
        devices=devices
    )
@app.route('/it_production/maintenance')
@authenticated
def it_production_maintenance():
    json_path = os.path.join(CURR_DIR, 'data/database.json')

    devices = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    devices = data.get("Maintenance", [])
            except json.JSONDecodeError:
                flash("Erreur de format dans le fichier JSON des appareils.", "danger")

    return render_template(
        'it-production.html',
        user=session['user'],
        active_tab='maintenance',
        devices=devices
    )

@app.route('/it_production/vendors')
@authenticated
def it_production_vendors():
    json_path = os.path.join(CURR_DIR, 'data/database.json')

    devices = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    devices = data.get("Vendors", [])
            except json.JSONDecodeError:
                flash("Erreur de format dans le fichier JSON des appareils.", "danger")

    return render_template(
        'it-production.html',
        user=session['user'],
        active_tab='vendors',
        devices=devices
    )

@app.route('/it_development')
@authenticated
def it_development_index():
    return render_template(
        'it-development.html',
        user=session['user'],
    )

@app.route('/it_development/inventory')
@authenticated
def it_development_inventory():
    json_path = os.path.join(CURR_DIR, 'data/database.json')

    devices = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    devices = data.get("Inventory", [])
            except json.JSONDecodeError:
                flash("Erreur de format dans le fichier JSON des appareils.", "danger")

    return render_template(
        'it-development.html',
        user=session['user'],
        active_tab='inventory',
        devices=devices
    )

@app.route('/it_development/maintenance')
@authenticated
def it_development_maintenance():
    json_path = os.path.join(CURR_DIR, 'data/database.json')

    devices = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    devices = data.get("Maintenance", [])
            except json.JSONDecodeError:
                flash("Erreur de format dans le fichier JSON des appareils.", "danger")

    return render_template(
        'it-development.html',
        user=session['user'],
        active_tab='maintenance',
        devices=devices
    )

@app.route('/it_development/vendors')
@authenticated
def it_development_vendors():
    json_path = os.path.join(CURR_DIR, 'data/database.json')

    devices = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    devices = data.get("Vendors", [])
            except json.JSONDecodeError:
                flash("Erreur de format dans le fichier JSON des appareils.", "danger")

    return render_template(
        'it-development.html',
        user=session['user'],
        active_tab='vendors',
        devices=devices
    )

@app.route('/it_devices')
@authenticated
def it_devices_index():
    return render_template(
        'it-devices.html',
        user=session['user'],
    )

@app.route('/it_devices/inventory')
@authenticated
def it_devices_inventory():
    json_path = os.path.join(CURR_DIR, 'data/database.json')

    devices = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    devices = data.get("Inventory", [])
            except json.JSONDecodeError:
                flash("Erreur de format dans le fichier JSON des appareils.", "danger")

    return render_template(
        'it-devices.html',
        user=session['user'],
        active_tab='inventory',
        devices=devices
    )


@app.route('/it_devices/maintenance')
@authenticated
def it_devices_maintenance():
    json_path = os.path.join(CURR_DIR, 'data/database.json')

    devices = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    devices = data.get("Maintenance", [])
            except json.JSONDecodeError:
                flash("Erreur de format dans le fichier JSON des appareils.", "danger")

    return render_template(
        'it-devices.html',
        user=session['user'],
        active_tab='maintenance',
        devices=devices
    )

@app.route('/it_devices/vendors')
@authenticated
def it_devices_vendors():
    json_path = os.path.join(CURR_DIR, 'data/database.json')

    devices = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            try:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    devices = data.get("Vendors", [])
            except json.JSONDecodeError:
                flash("Erreur de format dans le fichier JSON des appareils.", "danger")

    return render_template(
        'it-devices.html',
        user=session['user'],
        active_tab='vendors',
        devices=devices
    )


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
    flash('Logged out successfully!', 'success')
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
