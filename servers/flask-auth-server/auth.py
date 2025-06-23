from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from config import Config
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required", "error")
            return redirect(url_for('auth.register'))

        if User.find_by_username(username):
            flash("Username already exists", "error")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        User.create(username, hashed_password)
        flash("User registered successfully. Please log in.", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html') # Assuming a register.html will be created later

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required", "error")
            return render_template('login.html')

        user = User.get(username)
        if not user or not check_password_hash(user.hashed_password, password):
            flash("Invalid username or password", "error")
            return render_template('login.html')

        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(Config.STREAMLIT_APP_URL, code=302)
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/delete_user', methods=['POST'])
def delete_user_for_test():
    """
    Endpoint to delete a user, primarily for test cleanup.
    In a production environment, this would be secured or not exposed.
    """
    data = request.get_json()
    username = data.get('username')
    if username:
        if User.delete_user(username):
            return {"message": f"User {username} deleted (for test cleanup)"}, 200
        else:
            return {"message": f"User {username} not found or could not be deleted"}, 404
    return {"message": "Username not provided"}, 400