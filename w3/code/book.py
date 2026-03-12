from datetime import datetime
from flask import Flask, jsonify, request, make_response
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

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

def find_book_by_id(book_id):
    return next((b for b in books_db if b['id'] == book_id), None)

@app.route('/api/v1/books', methods=['GET'])
def get_books():
    response = wrap_with_metadata(books_db)
    response.headers['Cache-Control'] = 'public, max-age=30'
    return response, 200

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book_by_id(book_id)
    if not book:
        return wrap_with_metadata_error("book-not-found"), 404
    return wrap_with_metadata(book), 200

@app.route('/api/v1/books', methods=['POST'])
def create_book():
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

app.run(port=5000, debug=True)