import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS  # Importar CORS
from dotenv import load_dotenv





# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicialización de la aplicación y la base de datos
app = Flask(__name__)

CORS(app)  # Esto permite solicitudes desde cualquier origen (desarrollo)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de correo usando variables de entorno
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Inicialización de las extensiones
db = SQLAlchemy(app)
mail = Mail(app)

# Importar las rutas
from routes.contacto import contacto_bp
from routes.chatbot import chatbot_bp
# Registrar las rutas
app.register_blueprint(contacto_bp, url_prefix='/mensajes')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
