from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

from webhook_dispatcher import dispatch

app = Flask(__name__)
Swagger(app)

# --- books ---
books = []
next_id = 1

# --- webhook registry ---
webhooks = []
wh_next_id = 1

# --- test receiver storage ---
received_webhooks = []


def seed_data():
    global next_id
    for i, b in enumerate([
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "Sci-Fi"},
        {"title": "1984", "author": "George Orwell", "year": 1949, "genre": "Dystopian"},
        {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "genre": "Dystopian"},
        {"title": "Neuromancer", "author": "William Gibson", "year": 1984, "genre": "Sci-Fi"},
    ], 1):
        books.append({"id": i, **b})
        next_id = i + 1
        dispatch(webhooks, "book.created", books[-1])


def find_book(book_id):
    return next((b for b in books if b["id"] == book_id), None)


# ==================== Book CRUD ====================

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
    "summary": "Get a single book",
    "parameters": [{"name": "book_id", "in": "path", "type": "integer", "required": True}],
    "responses": {"200": {"description": "Book details"}, "404": {"description": "Not found"}},
})
def get_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Not found"}), 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
@swag_from({
    "tags": ["Books"],
    "summary": "Create book (triggers webhooks)",
    "parameters": [{
        "name": "body", "in": "body", "required": True,
        "schema": {
            "type": "object", "required": ["title", "author"],
            "properties": {
                "title": {"type": "string"}, "author": {"type": "string"},
                "year": {"type": "integer"}, "genre": {"type": "string"}, "isbn": {"type": "string"},
            },
        },
    }],
    "responses": {"201": {"description": "Created"}, "400": {"description": "Missing fields"}},
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
    dispatch(webhooks, "book.created", book)
    return jsonify(book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
@swag_from({
    "tags": ["Books"],
    "summary": "Update book (triggers webhooks)",
    "parameters": [
        {"name": "book_id", "in": "path", "type": "integer", "required": True},
        {"name": "body", "in": "body", "required": True,
         "schema": {"type": "object", "properties": {
             "title": {"type": "string"}, "author": {"type": "string"},
             "year": {"type": "integer"}, "genre": {"type": "string"}, "isbn": {"type": "string"},
         }}},
    ],
    "responses": {"200": {"description": "Updated"}, "404": {"description": "Not found"}},
})
def update_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body required"}), 400
    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    book["year"] = data.get("year", book["year"])
    book["genre"] = data.get("genre", book["genre"])
    book["isbn"] = data.get("isbn", book["isbn"])
    dispatch(webhooks, "book.updated", book)
    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Books"],
    "summary": "Delete book (triggers webhooks)",
    "parameters": [{"name": "book_id", "in": "path", "type": "integer", "required": True}],
    "responses": {"200": {"description": "Deleted"}, "404": {"description": "Not found"}},
})
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Not found"}), 404
    books.remove(book)
    dispatch(webhooks, "book.deleted", book)
    return jsonify({"message": "Deleted"}), 200


# ==================== Webhook Registry ====================

@app.route("/webhooks", methods=["GET"])
@swag_from({
    "tags": ["Webhooks"],
    "summary": "List all registered webhooks",
    "responses": {"200": {"description": "List of webhook subscriptions"}},
})
def get_webhooks():
    return jsonify(webhooks), 200


@app.route("/webhooks", methods=["POST"])
@swag_from({
    "tags": ["Webhooks"],
    "summary": "Register a webhook URL for an event",
    "parameters": [{
        "name": "body", "in": "body", "required": True,
        "schema": {
            "type": "object", "required": ["url", "event"],
            "properties": {
                "url": {"type": "string", "example": "http://localhost:5003/webhook-test-receiver"},
                "event": {"type": "string", "example": "book.created",
                         "enum": ["book.created", "book.updated", "book.deleted"]},
            },
        },
    }],
    "responses": {"201": {"description": "Webhook registered"}},
})
def create_webhook():
    global wh_next_id
    data = request.get_json()
    if not data or not data.get("url") or not data.get("event"):
        return jsonify({"error": "url and event required"}), 400
    wh = {"id": wh_next_id, "url": data["url"], "event": data["event"]}
    webhooks.append(wh)
    wh_next_id += 1
    return jsonify(wh), 201


@app.route("/webhooks/<int:wh_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Webhooks"],
    "summary": "Unregister a webhook",
    "parameters": [{"name": "wh_id", "in": "path", "type": "integer", "required": True}],
    "responses": {"200": {"description": "Webhook deleted"}, "404": {"description": "Not found"}},
})
def delete_webhook(wh_id):
    wh = next((w for w in webhooks if w["id"] == wh_id), None)
    if not wh:
        return jsonify({"error": "Webhook not found"}), 404
    webhooks.remove(wh)
    return jsonify({"message": "Webhook deleted"}), 200


# ==================== Test Receiver ====================

@app.route("/webhook-test-receiver", methods=["POST"])
@swag_from({
    "tags": ["Test"],
    "summary": "Local receiver for testing webhooks",
    "responses": {"200": {"description": "Webhook received"}},
})
def webhook_receiver():
    data = request.get_json()
    received_webhooks.append(data)
    print(f"[RECEIVER] Got webhook: {data['event']} — {data['data'].get('title', data['data'].get('id', ''))}")
    return jsonify({"status": "received"}), 200


@app.route("/webhook-test-receiver", methods=["GET"])
@swag_from({
    "tags": ["Test"],
    "summary": "List received webhooks",
    "responses": {"200": {"description": "Received webhook history"}},
})
def get_received_webhooks():
    return jsonify(received_webhooks), 200


if __name__ == "__main__":
    seed_data()
    app.run(debug=True, port=5003)
