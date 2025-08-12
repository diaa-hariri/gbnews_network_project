import sqlite3
from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.security import check_password_hash
from data.database import get_db_connection  # الاتصال بقاعدة البيانات

def login_user(request, session):
    if 'user' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # البحث عن المستخدم في قاعدة البيانات
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = {'email': user['email'], 'username': user['username']}
            flash('Connexion réussie !', 'success')
            return redirect(url_for('dashboard'))

        flash('Adresse e-mail ou mot de passe invalide', 'danger')

    return render_template('login.html')
