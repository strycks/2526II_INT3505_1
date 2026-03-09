from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

users = [{"id": 1, "name": "meepo"}]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if (request.method == 'GET'):
        response = make_response(jsonify({"users": users}))
        response.headers['Cache-Control'] = 'public, max-age=60'
        return response
    elif (request.method == 'POST'):
        new_user = request.get_json()
        users.append(new_user)
        return jsonify({"user": new_user}), 201
    
API_KEY = "super_secret"

@app.route('/secret', methods=['GET'])
def handle_secrets():
    client_key = request.headers.get('Authorization')
    
    if client_key == API_KEY:
        return 'secret information', 200
    else:
        return 'unauthorized', 401
app.run(debug=True)