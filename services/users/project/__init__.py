# services/users/project/__init__.py
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# instanciado la app
app = Flask(__name__)

# estabeciendo configuración
#app.config.from_object('project.config.DevelopmentConfig')

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# instanciando la
db = SQLAlchemy(app)

# modelo
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email



@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!!!'
        })