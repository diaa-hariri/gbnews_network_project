from flask import render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from config.firestore_db import db

def get_user_by_email(email):
    users_ref = db.collection('users').where('email', '==', email).limit(1).stream()
    for user in users_ref:
        return user.to_dict()  
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
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html')
