from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3
import hashlib

bp = Blueprint('registration', __name__)

@bp.route('/registration', methods=['GET', 'POST'])
def register():
    def create_users_table():
        with sqlite3.connect('user.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
            create table if not exists user (
                id integer primary key autoincrement,
                name text not null,
                contact text not null,
                email text not null unique,
                password text not null
            );
        """)
            conn.commit()

    create_users_table()

    if request.method == 'POST':
        name = request.form['full_name']
        contact = request.form['contact']
        email = request.form['email']
        password = request.form['create_password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = "Password and confirm password do not match. Please try again."
            return render_template('registration.html', error=error)

        # Encrypt the password using hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Create a new database connection
        with sqlite3.connect('user.db') as conn:
            cursor = conn.cursor()

            # Check if the email already exists
            cursor.execute("select * from user where email = ?", (email,))
            if cursor.fetchone():
                # If the email exists, redirect to the login page with a message
                # flash('An account with this email already exists. Please log in.', 'info')
                error="An account with this email already exists. Please log in."
                return render_template('registration.html', error=error)

            try:
                # Insert user data into the database
                cursor.execute("insert into user (name, contact, email, password) values (?, ?, ?, ?)", (name, contact, email, hashed_password))
                conn.commit()
                # flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('login'))
            except sqlite3.Error as e:
                print("Error while inserting user data into database:", e)
                # flash('An error occurred during registration. Please try again.', 'error')

    return render_template('registration.html')
