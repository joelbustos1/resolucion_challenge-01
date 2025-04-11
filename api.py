# api.py
from flask import Flask, request, jsonify
import jwt
import sqlite3
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')  # ahora configurable por variable de entorno

# --- Base de datos SQLite ---
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'user', 'user123')")
    conn.commit()
    conn.close()

init_db()

# --- Login ---
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # vulnerable a SQL injection
    c.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = c.fetchone()
    conn.close()

    if user:
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token if isinstance(token, str) else token.decode('utf-8')})
    return jsonify({'message': 'Credenciales inválidas'}), 401

# --- Endpoint protegido ---
@app.route('/userdata/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token requerido'}), 403

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        # no se verifica que el user_id del token coincida con el del request (IDOR)
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(f"SELECT id, username FROM users WHERE id = {user_id}")
        user = c.fetchone()
        conn.close()
        if user:
            return jsonify({'id': user[0], 'username': user[1]})
        return jsonify({'message': 'Usuario no encontrado'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido'}), 401

# --- Endpoint debug ---
@app.route('/debug', methods=['GET'])
def debug():
    return jsonify(dict(request.headers))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)