from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

MESSAGES = []
USERS = {}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    data = request.form.to_dict()
    username, password = data.values()

    if username in USERS and USERS.get(username, None) != password:
        return render_template("index.html", error="Incorrect password!")
    
    USERS[username] = password
    return render_template('chat.html', username=username)

@socketio.on('message')
def handle_message(message):
    MESSAGES.append({'username': message['username'],'message': message['text']})
    user = USERS.get(message['username'], False)
    if user:
        emit('message', {'username': user,
                         'text': message['text']}, broadcast=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0")