from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

app = Flask(__name__)
Swagger(app)

books = []
next_id = 1


def seed_data():
    global next_id
    samples = [
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "Sci-Fi", "isbn": "978-0441172719"},
        {"title": "1984", "author": "George Orwell", "year": 1949, "genre": "Dystopian", "isbn": "978-0451524935"},
        {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "genre": "Dystopian", "isbn": "978-0060850524"},
        {"title": "Neuromancer", "author": "William Gibson", "year": 1984, "genre": "Sci-Fi", "isbn": "978-0441569595"},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "genre": "Fantasy", "isbn": "978-0547928227"},
    ]
    for i, b in enumerate(samples, 1):
        books.append({"id": i, **b})
        next_id = i + 1


def find_book(book_id):
    return next((b for b in books if b["id"] == book_id), None)


@app.route("/books", methods=["GET"])
@swag_from({
    "tags": ["Books"],
    "summary": "List all books with optional filtering & search",
    "parameters": [
        {"name": "q", "in": "query", "type": "string", "description": "Search title/author"},
        {"name": "author", "in": "query", "type": "string", "description": "Filter by author (exact)"},
        {"name": "genre", "in": "query", "type": "string", "description": "Filter by genre (exact)"},
        {"name": "year", "in": "query", "type": "string", "description": "Filter by publication year"},
    ],
    "responses": {"200": {"description": "A list of books"}},
})
def get_books():
    q = request.args.get("q", "").lower()
    author = request.args.get("author", "").lower()
    genre = request.args.get("genre", "").lower()
    year = request.args.get("year")

    result = books
    if q:
        result = [b for b in result if q in b["title"].lower() or q in b["author"].lower()]
    if author:
        result = [b for b in result if b["author"].lower() == author]
    if genre:
        result = [b for b in result if b["genre"].lower() == genre]
    if year:
        result = [b for b in result if str(b["year"]) == year]

    return jsonify(result), 200


@app.route("/books/<int:book_id>", methods=["GET"])
@swag_from({
    "tags": ["Books"],
    "summary": "Get a single book by ID",
    "parameters": [
        {"name": "book_id", "in": "path", "type": "integer", "required": True},
    ],
    "responses": {
        "200": {"description": "Book details"},
        "404": {"description": "Book not found"},
    },
})
def get_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
@swag_from({
    "tags": ["Books"],
    "summary": "Create a new book",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["title", "author"],
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "year": {"type": "integer"},
                    "genre": {"type": "string"},
                    "isbn": {"type": "string"},
                },
            },
        },
    ],
    "responses": {
        "201": {"description": "Book created"},
        "400": {"description": "Missing required fields"},
    },
})
def create_book():
    global next_id
    data = request.get_json()
    if not data or not data.get("title") or not data.get("author"):
        return jsonify({"error": "title and author are required"}), 400

    book = {
        "id": next_id,
        "title": data["title"],
        "author": data["author"],
        "year": data.get("year"),
        "genre": data.get("genre"),
        "isbn": data.get("isbn"),
    }
    books.append(book)
    next_id += 1
    return jsonify(book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
@swag_from({
    "tags": ["Books"],
    "summary": "Update an existing book",
    "parameters": [
        {"name": "book_id", "in": "path", "type": "integer", "required": True},
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "year": {"type": "integer"},
                    "genre": {"type": "string"},
                    "isbn": {"type": "string"},
                },
            },
        },
    ],
    "responses": {
        "200": {"description": "Book updated"},
        "404": {"description": "Book not found"},
    },
})
def update_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    book["year"] = data.get("year", book["year"])
    book["genre"] = data.get("genre", book["genre"])
    book["isbn"] = data.get("isbn", book["isbn"])
    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Books"],
    "summary": "Delete a book",
    "parameters": [
        {"name": "book_id", "in": "path", "type": "integer", "required": True},
    ],
    "responses": {
        "200": {"description": "Book deleted"},
        "404": {"description": "Book not found"},
    },
})
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    books.remove(book)
    return jsonify({"message": "Book deleted"}), 200


if __name__ == "__main__":
    seed_data()
    app.run(debug=True, port=5001)
