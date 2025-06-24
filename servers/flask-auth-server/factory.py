import os
from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint

from config import Config
from auth import auth_bp
from models import User
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from clients.mongodb_client import MongoDBClient

def create_app():
    app = Flask(__name__)
    if os.environ.get('FLASK_ENV') == 'testing':
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY # Set a secret key for session management

    # Initialize MongoDBClient after app config is loaded
    mongo_client = MongoDBClient(base_url=app.config['MONGO_MCP_URL'])
    User.set_mongo_client(mongo_client)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Specify the login view

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @app.route('/protected')
    @login_required
    def protected():
        return "This is a protected route, accessible only to authenticated users!"

    return app

