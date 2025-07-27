import json
import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash

USERS_FILE = os.path.join('data', 'users.json')

def register_user(request):
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                users = json.load(f)
        else:
            users = []

        if any(user['email'] == email for user in users):
            flash('L\'adresse e-mail est déjà enregistrée. Veuillez utiliser une autre adresse e-mail.', 'danger')
            return redirect(request.url)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = {
            'email': email,
            'username': username,
            'password': hashed_password
        }
        users.append(new_user)

        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)

        flash('Utilisateur enregistré avec succès ! Veuillez vous connecter.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')
