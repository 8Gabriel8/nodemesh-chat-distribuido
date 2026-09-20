import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

messages = []

OTROS_NODOS = os.environ.get('OTROS_NODOS', '')
otros_nodos = [n.strip() for n in OTROS_NODOS.split(',') if n.strip()]

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    mensaje = data.get('mensaje')
    autor = data.get('autor', 'anonimo')

    if not mensaje:
        return jsonify({"error": "Falta el campo 'mensaje'"}), 400

    nuevo_mensaje = {"autor": autor, "mensaje": mensaje}
    messages.append(nuevo_mensaje)

    for nodo in otros_nodos:
        try:
            requests.post(f"{nodo}/receive", json=nuevo_mensaje, timeout=2)
        except requests.exceptions.RequestException:
            print(f"No se pudo contactar a {nodo}")

    return jsonify({"status": "ok", "mensaje_guardado": nuevo_mensaje}), 201

@app.route('/receive', methods=['POST'])
def receive_message():
    data = request.get_json()
    mensaje = data.get('mensaje')
    autor = data.get('autor', 'anonimo')

    nuevo_mensaje = {"autor": autor, "mensaje": mensaje}
    messages.append(nuevo_mensaje)

    return jsonify({"status": "recibido"}), 201

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages), 200

if __name__ == '__main__':
    puerto = int(os.environ.get('PUERTO', 5001))
    app.run(host='0.0.0.0', port=puerto, debug=True)
