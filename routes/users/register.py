from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from config.firestore_db import db

def register_user(request):
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        existing_user = db.collection('users').where('email', '==', email).limit(1).stream()

        if any(existing_user):
            flash('Email is already registered. Please use a different email.', 'danger')
            return redirect(request.url)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        user_ref = db.collection('users').add({
            'email': email,
            'username': username,
            'password': hashed_password,
        })

        flash('User registered successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')
