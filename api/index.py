import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Blueprints
    from routes.auth_routes import auth_bp
    from routes.admin_routes import admin_bp
    from routes.mahasiswa_routes import mahasiswa_bp
    from routes.ujian_routes import ujian_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(mahasiswa_bp)
    app.register_blueprint(ujian_bp)

    # Import models for migration
    from models import user_model, soal_model, hasil_model

    @app.errorhandler(404)
    def page_not_found(e):
        return "404 Not Found", 404

    return app

# Vercel handler
app = create_app()

def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)