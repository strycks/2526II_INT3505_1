from flask import Flask, jsonify, request

app = Flask(__name__)

users = [{"id": 1, "name": "meepo"}]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if (request.method == 'GET'):
        return jsonify({"users": users}), 200
    elif (request.method == 'POST'):
        new_user = request.get_json()
        users.append(new_user)
        return jsonify({"user": new_user}), 201
    
app.run(debug=True)