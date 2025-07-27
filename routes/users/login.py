import json
import os
from flask import render_template, redirect, url_for, flash, session

from werkzeug.security import check_password_hash

USERS_FILE = os.path.join('data', 'users.json')

def get_user_by_email(email):
    if not os.path.exists(USERS_FILE):
        return None

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
        for user in users:
            if user['email'] == email:
                return user
    return None

def login_user(request, session):
    if 'user' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user'] = {'email': email, 'username': user['username']}
            flash('Connexion réussie !', 'success')
            return redirect(url_for('dashboard'))

        flash('Adresse e-mail ou mot de passe invalide', 'danger')

    return render_template('login.html')
