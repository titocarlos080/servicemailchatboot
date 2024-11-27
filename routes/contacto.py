from flask import Blueprint, request, jsonify
from flask_mail import Message
from app import db, mail
import os

contacto_bp = Blueprint('contacto', __name__)

# Ruta para recibir los mensajes
@contacto_bp.route('', methods=['POST'])
def recibir_mensaje():
    # Obtener los datos del formulario
    nombre = request.json.get('name')
    correo = request.json.get('email')
    mensaje = request.json.get('message')
    if not nombre or not correo or not mensaje:
        return jsonify({'error': 'Faltan datos'}), 400

    # Guardar en la base de datos
    nuevo_contacto = Contacto(nombre=nombre, correo=correo, mensaje=mensaje)
    db.session.add(nuevo_contacto)
    db.session.commit()
    
    # Enviar un correo de notificación
    try:
        msg = Message('Nuevo mensaje de contacto',
                      sender=os.getenv('MAIL_USERNAME'),
                      recipients=[os.getenv('MAIL_USERNAME')])
        msg.body = f'Nombre: {nombre}\nCorreo: {correo}\nMensaje: {mensaje}'
        mail.send(msg)

    except Exception as e:
        return jsonify({'error': 'No se pudo enviar el correo', 'details': str(e)}), 500

    return jsonify({'message': 'Mensaje recibido y notificación enviada'}), 200

# Modelo para la base de datos
class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
