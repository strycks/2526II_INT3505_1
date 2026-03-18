from datetime import datetime
from flask import Flask, jsonify, request, make_response
from flasgger import Swagger
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

template = {
    "info": {
        "title": "Book Management API",
    },
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
    "security": [ 
        {"bearerAuth": []}
    ],
}
app.config['SWAGGER'] = {
    'title': 'Book API Docs',
    'uiversion': 3,
    'openapi': '3.0.3'
}
swagger = Swagger(app, template=template)

app.config["JWT_SECRET_KEY"] = "tXHzZyrglpWqIgfONgcI+gsoCnXKhFFRsFsLtfx0JqU=" 
jwt = JWTManager(app)

books_db = [
    {"id": 1, "title": "the art of war", "author": "sun tzu", "year": 450},
    {"id": 2, "title": "the c programming language", "author": "brian kernighan", "year": 1978}
]

def wrap_with_metadata(data):
    return jsonify({
        "metadata": {
            "apiVersion": "1.0",
            "timestamp": datetime.now().isoformat()
        },
        "data": data
    })

def wrap_with_metadata_error(error):
    return jsonify({
        "metadata": {
            "apiVersion": "1.0",
            "timestamp": datetime.now().isoformat()
        },
        "error": error
    })
    
@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    """
    Login
    ---
    tags: [Authentication]
    security: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: {type: string}
              password: {type: string}
    security: []
    responses:
      200:
        description: Return a JWT token
      401:
        description: Invalid credentials
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if username != "admin" or password != "123456":
        return wrap_with_metadata_error("invalid-credentials"), 401

    access_token = create_access_token(identity=username)
    return wrap_with_metadata(access_token), 200

def find_book_by_id(book_id):
    return next((b for b in books_db if b['id'] == book_id), None)

@app.route('/api/v1/books', methods=['GET'])
def get_books():
    """
    Get all books
    ---
    tags: [Books]
    security: []
    responses:
      200:
        description: OK
    """
    response = wrap_with_metadata(books_db)
    response.headers['Cache-Control'] = 'public, max-age=30'
    return response, 200

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    """
    Get a specific book by ID
    ---
    tags: [Books]
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: OK
    """
    book = find_book_by_id(book_id)
    if not book:
        return wrap_with_metadata_error("book-not-found"), 404
    return wrap_with_metadata(book), 200

@app.route('/api/v1/books', methods=['POST'])
@jwt_required()
def create_book():
    """
    Create a new book
    ---
    tags: [Books]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title: {type: string}
              author: {type: string}
              year: {type: integer}
    responses:
      201:
        description: Successfully created
    """
    if not request.json or 'title' not in request.json:
        return wrap_with_metadata_error("bad-request"), 400
    
    new_book = {
        "id": books_db[-1]['id'] + 1 if books_db else 1,
        "title": request.json['title'],
        "author": request.json.get('author', "Unknown"),
        "year": request.json.get('year', 2024)
    }
    books_db.append(new_book)
    return wrap_with_metadata(new_book), 201

@app.errorhandler(404)
def not_found(error):
    return wrap_with_metadata_error("not-found"), 404

if __name__ == "__main__":
    app.run(port=5000, debug=True)