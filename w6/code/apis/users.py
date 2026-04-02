from datetime import datetime
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields, Resource
from utils import wrap_with_metadata, wrap_with_metadata_error, cursor_pagination_parser
from database import users_db, borrows_db, books_db

ns_users = Namespace('api/v1/users', description='User Management')

user_model = ns_users.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'name': fields.String(required=True)
})

borrow_model = ns_users.model('Borrow', {
    'book_id': fields.Integer(required=True),
    'user_id': fields.Integer(required=True)
})

borrow_request_model = ns_users.model('BorrowRequest', {
    'book_id': fields.Integer(required=True)
})

@ns_users.route('')
class UserList(Resource):
    @jwt_required()
    @ns_users.expect(cursor_pagination_parser)
    def get(self):
        """Get all users"""
        args = cursor_pagination_parser.parse_args()
        after_id = args['after']
        limit = args['limit']
        
        start_idx = -1
        for index, user in enumerate(users_db):
            if user['id'] >= after_id:
                start_idx = index
                break
            
        if start_idx == -1: 
            return wrap_with_metadata([]), 200
        
        items = users_db[start_idx : start_idx + limit]
        pagination = {
            "type": "cursor-based",
            "links": {
                "cur": f"?after={after_id}&limit={limit}",
                "next": f"?after={items[-1]['id'] + 1}&limit={limit}" if start_idx + limit < len(users_db) else None
            }
        }
        return wrap_with_metadata(items, pagination), 200
    
@ns_users.route('/<int:user_id>')
class UserEntry(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get a specific user"""
        user = next((u for u in users_db if u['id'] == user_id), None)
        if not user:
            return wrap_with_metadata_error("user-not-found"), 404
        return wrap_with_metadata(user)

@ns_users.route('/<int:user_id>/borrows')
class UserBorrows(Resource):
    @jwt_required()
    def get(self, user_id):
        """View list of borrowed books"""
        user_borrows = [b for b in borrows_db if b['user_id'] == user_id]
        
        result = []
        # Replicate JOIN statement
        for b in user_borrows:
            book = next((book for book in books_db if book['id'] == b['book_id']), None)
            book["borrow_date"] = b["borrow_date"]
            result.append(book)
        return wrap_with_metadata(result), 200

    @jwt_required()
    @ns_users.expect(borrow_request_model)
    def post(self, user_id):
        """Borrow a book"""
        data = request.json
        book_id = data.get('book_id')
        
        book = next((b for b in books_db if b['id'] == book_id), None)
        user = next((u for u in users_db if u['id'] == user_id), None)
        if not book:
            return wrap_with_metadata_error("book-not-found"), 404
        if not user:
            return wrap_with_metadata_error("user-not-found"), 404
        
        new_borrow = {
            "user_id": user_id,
            "book_id": book_id,
            "borrow_date": datetime.now().isoformat()
        }
        borrows_db.append(new_borrow)
        return wrap_with_metadata(new_borrow), 201