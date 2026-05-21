from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from event_bus import EventBus
from handlers import audit_logger, search_indexer, get_indexed_titles, audit_log

app = Flask(__name__)
Swagger(app)

bus = EventBus()
bus.subscribe("book.created", audit_logger)
bus.subscribe("book.updated", audit_logger)
bus.subscribe("book.deleted", audit_logger)
bus.subscribe("book.created", search_indexer)
bus.subscribe("book.updated", search_indexer)
bus.subscribe("book.deleted", search_indexer)

books = []
next_id = 1


def seed_data():
    global next_id
    samples = [
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "Sci-Fi"},
        {"title": "1984", "author": "George Orwell", "year": 1949, "genre": "Dystopian"},
        {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "genre": "Dystopian"},
        {"title": "Neuromancer", "author": "William Gibson", "year": 1984, "genre": "Sci-Fi"},
    ]
    for i, b in enumerate(samples, 1):
        book = {"id": i, **b}
        books.append(book)
        next_id = i + 1
        bus.publish("book.created", book)


def find_book(book_id):
    return next((b for b in books if b["id"] == book_id), None)


@app.route("/books", methods=["GET"])
@swag_from({
    "tags": ["Books"],
    "summary": "List books with optional filtering",
    "parameters": [
        {"name": "q", "in": "query", "type": "string"},
        {"name": "genre", "in": "query", "type": "string"},
    ],
    "responses": {"200": {"description": "List of books"}},
})
def get_books():
    q = request.args.get("q", "").lower()
    genre = request.args.get("genre", "").lower()

    result = books
    if q:
        result = [b for b in result if q in b["title"].lower() or q in b["author"].lower()]
    if genre:
        result = [b for b in result if b["genre"].lower() == genre]
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
        return jsonify({"error": "Not found"}), 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
@swag_from({
    "tags": ["Books"],
    "summary": "Create a new book (emits book.created event)",
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
        return jsonify({"error": "title and author required"}), 400

    book = {"id": next_id, "title": data["title"], "author": data["author"],
            "year": data.get("year"), "genre": data.get("genre"), "isbn": data.get("isbn")}
    books.append(book)
    next_id += 1

    bus.publish("book.created", book)
    return jsonify(book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
@swag_from({
    "tags": ["Books"],
    "summary": "Update a book (emits book.updated event)",
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
        "400": {"description": "Missing request body"},
        "404": {"description": "Book not found"},
    },
})
def update_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    book["year"] = data.get("year", book["year"])
    book["genre"] = data.get("genre", book["genre"])
    book["isbn"] = data.get("isbn", book["isbn"])

    bus.publish("book.updated", book)
    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Books"],
    "summary": "Delete a book (emits book.deleted event)",
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
        return jsonify({"error": "Not found"}), 404
    books.remove(book)
    bus.publish("book.deleted", book)
    return jsonify({"message": "Deleted"}), 200


@app.route("/events/audit", methods=["GET"])
@swag_from({
    "tags": ["Events"],
    "summary": "View audit log (built from events)",
    "responses": {"200": {"description": "List of audit entries"}},
})
def get_audit_log():
    return jsonify(audit_log), 200


@app.route("/events/search-index", methods=["GET"])
@swag_from({
    "tags": ["Events"],
    "summary": "View search index (built from events)",
    "responses": {"200": {"description": "Indexed book IDs"}},
})
def get_search_index():
    return jsonify({"indexed_ids": get_indexed_titles()}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5002)
