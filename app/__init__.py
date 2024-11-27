from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Inicialización de extensiones
db = SQLAlchemy()
mail = Mail()

def create_app():
    # Crear aplicación
    app = Flask(__name__)
    load_dotenv()

    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    # Inicializar extensiones
    db.init_app(app)
    mail.init_app(app)
    CORS(app, origins=["https://surbug.netlify.app", "http://localhost:5000", "http://127.0.0.1:5000"])
    # Registrar rutas
    with app.app_context():
        from app.routes.contacto import contacto_bp
        from app.routes.chatbot import chatbot_bp
        app.register_blueprint(contacto_bp, url_prefix='/mensajes')
        app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
        db.create_all()

    return app
