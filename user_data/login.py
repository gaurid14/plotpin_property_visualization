from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib

bp = Blueprint('login', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Encrypt the password using hashlib with a salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            # Create a new database connection
            with sqlite3.connect('user.db') as conn:
                cursor = conn.cursor()
                # Retrieve user data from the database
                cursor.execute("select * from user where email = ? and password = ?", (email, hashed_password))
                row = cursor.fetchone()

                if row:
                    # Store email in session
                    session['email'] = email
                    return render_template('home.html', email=email)
                else:
                    # User does not exist or password is incorrect
                    # flash('Invalid email or password. Please try again or register if you are a new user.', 'error')
                    return render_template('login.html', error='Invalid email or password. Please try again or register if you are a new user')
        except sqlite3.Error as e:
            print("Error while querying user data from database:", e)
            flash('An error occurred while logging in. Please try again.', 'error')
            return render_template('login.html')

    return render_template('login.html')
