import uuid
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

MESSAGES = []
USERS = {}
SECRETS = {}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    data = request.form.to_dict()
    username, password = data.get('username'), data.get('password')

    if not username or not password:
        return render_template("index.html", error="Username and password are required!")

    if username in USERS:
        if USERS[username]['password'] != password:
            return render_template("index.html", error="Incorrect password!")
    else:
        user_secret = str(uuid.uuid4())
        USERS[username] = {'secret': user_secret, 'password': password}
        SECRETS[user_secret] = username

    return render_template(
        'chat.html',
        username=username,
        secret=USERS[username]['secret'],
        messages=MESSAGES
    )

@socketio.on('message')
def handle_message(message):
    username = SECRETS.get(message.get('secret'))
    if username:
        msg = {'username': username, 'text': message.get('text', '')}
        MESSAGES.append(msg)
        emit('message', msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")