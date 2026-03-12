from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

users = [{"id": 1, "name": "meepo"}]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    # curl "http://127.0.0.1:5000/users"
    if (request.method == 'GET'):
        response = make_response(jsonify({"users": users}))
        response.headers['Cache-Control'] = 'public, max-age=60'
        return response
    # curl -X POST "http://127.0.0.1:5000/users" -d '{"id": "2", "name": "invoker"}' -H "Content-Type: application/json"
    elif (request.method == 'POST'):
        new_user = request.get_json()
        users.append(new_user)
        return jsonify({"user": new_user}), 201
    
API_KEY = "super_secret"

@app.route('/secret', methods=['GET'])
def handle_secrets():
    # curl "http://127.0.0.1:5000/secret" -H "Authorization: super_secret"
    client_key = request.headers.get('Authorization')
    
    if client_key == API_KEY:
        return 'secret information', 200
    else:
        return 'unauthorized', 401

app.run(debug=True)