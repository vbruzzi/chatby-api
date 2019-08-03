from flask import Flask, jsonify, request, redirect, url_for
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
from bson import ObjectId
from os import environ
import os
import datetime
import json
import hashlib
import markdown

# Encryption Salt
SALT = "thisistheSALT"
# Mongo URI
mongoURI = os.environ['connectionstring']
client = MongoClient(mongoURI)
#Use this to connect via environment variable
#client = MongoClient(environ["connectionstring"])
db = client.Chatby

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)


# CHAT RELATED ROUTES

@app.route('/', methods=["GET"])
def redirect_chat():
        return redirect(url_for('chat'))

@app.route('/chat', methods=["GET", "POST"])
def chat():
        col = db.Chat
        # Posts a new message to the chat collection
        if request.method == "POST":
                try: 
                        # Gets the message from json request and formats it for insertion
                        newMessage = request.get_json()       
                        formattedMessage = {'message': newMessage['message'], 'username': newMessage['username'], 'created': datetime.datetime.now()} 
                        col.insert_one(formattedMessage)
                        return '', 201
                except Exception as ex:
                        return ex, 500

        # Gets all messages from the chat collection
        elif request.method == "GET":
                try:
                        getNotes = col.find()
                        # Returns a list of all messages
                        notes = [{'message': x['message'], 'username': x['username']} for x in getNotes] 
                        return jsonify(notes), 200
                except Exception as ex:
                        return ex, 500
        # Unsupported method
        else: 
                return "Method not supported", 405



# USER RELATED ROUTES

# Searches database if user exists
def search(data):
        col = db.Users
        user = col.find_one(data)
        # Returns true if the user exists
        if user is not None: 
                return user
        return False

# Hashes password
def hashpassword(password):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT.encode('utf-8'), 10000)


@app.route('/user', methods=["POST", "GET"])
def users():
        col = db.Users
        # Expects JSON data, stylized is how it's spelled, username is the database value used for checking
        if request.is_json:
                inputtedData = request.get_json()
        else:
                inputtedData = {
                        'username': request.args.get('username'),
                        'password': request.args.get('password')}

        username = inputtedData['username'].lower()
        stylizedUsername = inputtedData['username']
        password = inputtedData['password']

        # Register
        if request.method == 'POST':
                try:    
                        # Checks if user already exists
                        if search({'username': username}):
                                return 'User already exists', 409
                        else:
                                password = hashpassword(password)
                                col.insert_one({'username':username, 'stylizedUsername': stylizedUsername, 'password':password, 'messagesSent': 0})
                                return '', 201
                                
                except Exception as e:
                        return str(e), 500
        
        # Login
        elif request.method == 'GET':
                try:
                        password = hashpassword(password)
                        data={'username': username, 'password':password}
                        # Checks if user exists
                        checkUser = search(data)
                        if checkUser:
                                returnUser = {'username': checkUser['username'], 'stylizedUsername': checkUser['stylizedUsername']}
                                return jsonify(returnUser), 200
                        else:
                                return 'User with these credentials does not exist', 404
                except Exception as e:
                        return str(e), 500

        # Not yet implemented requests (such as UPDATE)
        else:
                return 'Method not supported', 405
        

@socketio.on('connection', namespace='/')
def test_connect():
    print("A user has connected")

@socketio.on('message')
def handle_message(message):
        emit('message', message, broadcast=True)
        
    
if __name__ == '__main__':
        socketio.run(app)