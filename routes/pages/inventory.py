from flask import Blueprint, render_template, session, redirect, url_for, flash, request
import os
import json
from functools import wraps

inventory_bp = Blueprint('inventory', __name__)

CURR_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
def authenticated(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner_func

@inventory_bp.route('/inventory')
@authenticated
def inventory():
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
        'sections/inventory.html',
        user=session['user'],
        devices=devices
    )

@inventory_bp.route('/run_scan', methods=['POST'])
@authenticated
def run_scan():
    try:
        script_path = os.path.join(CURR_DIR, 'scripts/generate_devices_json.py')
        result = os.system(f'python3 "{script_path}"')
        if result == 0:
            flash("✅ Analyse du réseau terminée avec succès. Le fichier a été mis à jour.", "success")
        else:
            flash("❌ Échec de l'exécution du script d'analyse réseau.", "danger")
    except Exception as e:
        flash(f"❌ Erreur lors de l'exécution de l'analyse : {str(e)}", "danger")

    return redirect(url_for('inventory.inventory'))
