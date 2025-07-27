import json
import os
from datetime import datetime
from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from functools import wraps

it_development_bp = Blueprint('it_development', __name__, url_prefix='/it_development')

def authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'services_development.json')
DATABASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database.json')
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'users.json')

@it_development_bp.route('/', methods=['GET', 'POST'])
@authenticated
def it_development_index():
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            database_data = json.load(f)
            inventory_items = database_data.get('Inventory', [])
            device_names = [item.get('name') for item in inventory_items if 'name' in item]
    except (FileNotFoundError, json.JSONDecodeError):
        device_names = []

    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            user_list = [user.get('username') or user.get('email') for user in users_data]
    except (FileNotFoundError, json.JSONDecodeError):
        user_list = []

    if request.method == 'POST':
        service_name = request.form.get('service_name')
        service_description = request.form.get('service_description')
        selected_device_name = request.form.get('device_name')
        assigned_to = request.form.get('assigned_to')  

        user = session['user'].get('displayName') or session['user'].get('username') or 'Utilisateur inconnu'
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                services = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            services = []

        new_service = {
            'nom_service': service_name,
            'description_service': service_description,
            'device_name': selected_device_name,
            'date_ajout': date_added,
            'ajoute_par': user,
            'assigne_a': assigned_to 
        }
        services.append(new_service)

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(services, f, ensure_ascii=False, indent=4)

        flash('Service ajouté avec succès!', 'success')
        return redirect(url_for('it_development.it_development_index'))

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            services = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        services = []

    return render_template(
        'sections/it-development.html',
        user=session['user'],
        services=services,
        device_names=device_names,
        user_list=user_list 
    )