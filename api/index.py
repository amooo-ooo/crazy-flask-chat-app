from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

MESSAGES = {}
USERS = {}
 
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    data = request.form.to_dict()
    username, password = data.values()
    
    if username in USERS and USERS.get(username, None) != password:
        return render_template("index.html",
                               error="Incorrect password!")
    USERS[username] = password
    return render_template('chat.html',
                           username=username)

@socketio.on('message')
def handle_message(message):
    # MESSAGES.append({'username': message['username'], 'message': message['text']})
    emit('message', {'username': message['username'], 
                     'text': message['text']}, broadcast=True)
