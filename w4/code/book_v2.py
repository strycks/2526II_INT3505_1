from datetime import datetime
from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

authorizations = {
    "bearerAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

api = Api(app, 
    version='1.0', 
    title='Book Management API',
    authorizations=authorizations,
    security='bearerAuth',
    doc='/apidocs/'
)

app.config["JWT_SECRET_KEY"] = "tXHzZyrglpWqIgfONgcI+gsoCnXKhFFRsFsLtfx0JqU=" 
jwt = JWTManager(app)

books_db = [
    {"id": 1, "title": "the art of war", "author": "sun tzu", "year": 450},
    {"id": 2, "title": "the c programming language", "author": "brian kernighan", "year": 1978}
]

login_model = api.model('Login', {
    'username': fields.String(required=True, default='admin'),
    'password': fields.String(required=True, default='123456')
})

book_model = api.model('Book', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(required=True),
    'author': fields.String(default="Unknown"),
    'year': fields.Integer(default=2026)
})

def wrap_with_metadata(data):
    return {
        "metadata": {
            "apiVersion": "1.0",
            "timestamp": datetime.now().isoformat()
        },
        "data": data
    }

def wrap_with_metadata_error(error):
    return {
        "metadata": {
            "apiVersion": "1.0",
            "timestamp": datetime.now().isoformat()
        },
        "error": error
    }

ns_auth = api.namespace('api/v1/auth', description='Authorization')
ns_books = api.namespace('api/v1/books', description='Book Management')

@ns_auth.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.doc(security=[])
    def post(self):
        """Login to get JWT Token"""
        data = request.json
        username = data.get("username")
        password = data.get("password")
        
        if username != "admin" or password != "123456":
            return wrap_with_metadata_error("invalid-credentials"), 401

        access_token = create_access_token(identity=username)
        return wrap_with_metadata(access_token), 200

@ns_books.route('')
class BookList(Resource):
    @jwt_required()
    def get(self):
        """Get all books"""
        return wrap_with_metadata(books_db), 200

    @jwt_required()
    @api.expect(book_model)
    @api.response(201, 'Created')
    def post(self):
        """Add new book"""
        data = request.json
        if not data or 'title' not in data:
            return wrap_with_metadata_error("bad-request"), 400
        
        new_book = {
            "id": books_db[-1]['id'] + 1 if books_db else 1,
            "title": data['title'],
            "author": data.get('author', "Unknown"),
            "year": data.get('year', 2026)
        }
        books_db.append(new_book)
        return wrap_with_metadata(new_book), 201

@ns_books.route('/<int:book_id>')
class BookItem(Resource):
    @jwt_required()
    def get(self, book_id):
        """Get a specific book"""
        book = next((b for b in books_db if b['id'] == book_id), None)
        if not book:
            return wrap_with_metadata_error("book-not-found"), 404
        return wrap_with_metadata(book), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)