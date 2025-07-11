from flask import Blueprint, session, url_for, redirect

bp = Blueprint('session', __name__)

@bp.route('/')
def index():
    if 'email' in session:
        return f'Logged in as {session["email"]}'
    return redirect(url_for('home'))

@bp.route('/logout')
def logout():
    session.pop('email', None)  # Remove the 'username' key from the session
    return redirect(url_for('home'))
