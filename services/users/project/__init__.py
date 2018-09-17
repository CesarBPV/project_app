# services/users/project/__init__.py

from flask import Flask, jsonify


# instanciado la app
app = Flask(__name__)

# estabeciendo configuración
app.config.from_object('project.config.DevelopmentConfig')

@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!!!'
        })