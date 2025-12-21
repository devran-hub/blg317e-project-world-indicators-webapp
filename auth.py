"""
Authentication module for admin panel
Database-backed session authentication
"""

from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash


import json
import os

def load_users():
    """Load users from users.json"""
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)
            return data.get('users', [])
    except FileNotFoundError:
        return []

def register_user(username, email, password):
    """Register a new user"""
    db = {'users': load_users()}
    
    # Check if user already exists
    for user in db['users']:
        if user['username'] == username:
            return False, "Username already exists"
        if user.get('email') == email:
            return False, "Email already exists"
            
    # Add new user
    new_user = {
        "username": username,
        "email": email,
        "password_hash": generate_password_hash(password, method='pbkdf2:sha256'),
        "role": "admin",
        "is_approved": False  # New users require approval
    }
    
    db['users'].append(new_user)
    
    try:
        with open('users.json', 'w') as f:
            json.dump(db, f, indent=4)
        return True, "Registration successful"
    except Exception as e:
        return True, "Registration successful"
    except Exception as e:
        return False, f"Error saving user: {str(e)}"

def login_user(username, password):
    """Authenticate user against users.json and create session"""
    users = load_users()
    
    user = next((u for u in users if u['username'] == username), None)
    
    if user and check_password_hash(user['password_hash'], password):
        if not user.get('is_approved', False):
            return False, "Your account is pending approval."
            
        session['logged_in'] = True
        session['username'] = username
        session['role'] = user['role']
        return True, "Login successful"
    return False, "Invalid username or password"

def get_pending_users():
    """Get list of users pending approval"""
    users = load_users()
    return [u for u in users if not u.get('is_approved', False)]

def approve_user(username):
    """Approve a pending user"""
    db = {'users': load_users()}
    updated = False
    
    for user in db['users']:
        if user['username'] == username:
            user['is_approved'] = True
            updated = True
            break
            
    if updated:
        try:
            with open('users.json', 'w') as f:
                json.dump(db, f, indent=4)
            return True, "User approved successfully"
        except Exception as e:
            return False, f"Error saving user: {str(e)}"
    return False, "User not found"

def reject_user(username):
    """Reject (delete) a pending user"""
    db = {'users': load_users()}
    initial_count = len(db['users'])
    
    # Filter out the rejected user
    db['users'] = [u for u in db['users'] if u['username'] != username]
    
    if len(db['users']) < initial_count:
        try:
            with open('users.json', 'w') as f:
                json.dump(db, f, indent=4)
            return True, "User rejected and removed"
        except Exception as e:
            return False, f"Error saving changes: {str(e)}"
    return False, "User not found"

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
