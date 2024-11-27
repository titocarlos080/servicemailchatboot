from flask import Blueprint, request, jsonify
import os
import requests  # Asegúrate de tener esta librería importada

chatbot_bp = Blueprint('chatbot', __name__)

# Ruta para interpretar chatbot IA
@chatbot_bp.route('', methods=['POST'])
def chatbot():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'El mensaje está vacío.'}), 400

    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
        'Content-Type': 'application/json'
    }
    
    # Construir el mensaje para el comportamiento
    prompt_message = getcomportamiento(message)

    request_body = {
        "model": "gpt-3.5-turbo",  
        "messages": [
            {"role": "system", "content": "Eres un asistente virtual de la empresa de desarrollo de SURBUG. Solo puedes responder sobre tecnología, desarrollo de software, mantenimiento de sistemas y asesoramiento IT."},
            {"role": "user", "content": prompt_message}
        ]
    }

    try:
        # Realizar la solicitud POST a la API de OpenAI
        response = requests.post(url, json=request_body, headers=headers)
        
        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            chat_response = response.json()
            reply = chat_response['choices'][0]['message']['content'].strip()
            return jsonify({'reply': reply})
        else:
            return jsonify({'error': 'Error al obtener la respuesta de la API de OpenAI'}), 500

    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API de ChatGPT: {e}")
        return jsonify({'error': 'Hubo un error al procesar la solicitud.'}), 500


def getcomportamiento(text):
    """
    Esta función genera el mensaje a partir de lo que el usuario escribió,
    proporcionando ejemplos predefinidos de posibles respuestas.
    """
    # Filtramos las preguntas no relacionadas con tecnología
    prompt_message = f"""
    Aquí está el esquema de posibles respuestas:
    msg:Hola  resp: Hola Bienvenido a SURBUG, ¿en qué te puedo ayudar?
    msg:Ayuda  resp: Claro, ¿cómo puedo asistirte hoy?
    msg:Servicios  resp: Ofrecemos desarrollo de software, mantenimiento de sistemas y asesoramiento en IT.
    
    # Agregamos un filtro para manejar solicitudes fuera del contexto de la empresa
    msg:¿Sabes de carnicerías?  resp: Lo siento, no puedo responder preguntas sobre carnicerías. Soy un asistente de tecnología y desarrollo de software.

    si el mensaje está fuera del contexto de la empresa, responde algo como: 
    "Lo siento, solo puedo hablar sobre tecnología, desarrollo de software y servicios relacionados. ¿En qué puedo ayudarte con eso?"

    El usuario ha solicitado lo siguiente:
    {text}, responde con respuestas cortas y amables, asegurándote de que la respuesta sea siempre dentro del contexto empresarial.
    """
    return prompt_message 
