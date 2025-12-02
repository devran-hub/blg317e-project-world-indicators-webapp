"""
Authentication module for admin panel
Database-backed session authentication
"""

from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from db_utils import execute

def login_user(username, password):
    """Authenticate user against database and create session"""
    user = execute(
        "SELECT * FROM Users WHERE username = %s",
        (username,),
        fetch=True
    )
    
    if user and check_password_hash(user[0]['password_hash'], password):
        session['logged_in'] = True
        session['username'] = username
        session['role'] = user[0]['role']
        return True
    return False

def logout_user():
    """Clear session"""
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('role', None)

def is_logged_in():
    """Check if user is logged in"""
    return session.get('logged_in', False)

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please login to access this feature.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
