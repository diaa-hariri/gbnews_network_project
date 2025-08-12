import sqlite3
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from data.database import get_db_connection  # تأكد من استيراد الاتصال بالقاعدة

def register_user(request):
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # تأكد من عدم وجود نفس الإيميل مسبقًا
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("L'adresse e-mail est déjà enregistrée. Veuillez utiliser une autre adresse e-mail.", 'danger')
            conn.close()
            return redirect(request.url)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # إدخال المستخدم في القاعدة
        cursor.execute('''
            INSERT INTO users (email, username, password)
            VALUES (?, ?, ?)
        ''', (email, username, hashed_password))
        conn.commit()
        conn.close()

        flash("Utilisateur enregistré avec succès ! Veuillez vous connecter.", 'success')
        return redirect(url_for('login'))

    return render_template('register.html')
