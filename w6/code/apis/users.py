from datetime import datetime
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields, Resource
from utils import wrap_with_metadata, wrap_with_metadata_error, cursor_pagination_parser, wrap_with_metadata_v2
from database import users_db, borrows_db, books_db
from models import User, Book, Borrowing
<<<<<<< HEAD
from apis.books import book_model
=======
>>>>>>> b3debb05987147f8ccaf8d884e04105f1827165a

ns_users = Namespace('api/v1/users', description='User Management')

user_model = ns_users.model('User', {
    'id': fields.String(required=True),
    'username': fields.String(required=True),
    'name': fields.String(required=True)
})

<<<<<<< HEAD
borrowing_model = ns_users.model('Borrowing', {
    'book': fields.Nested(book_model),
})

borrowing_request_model = ns_users.model('BorrowingRequest', {
=======
borrowing_model = ns_users.model('Borrow', {
    'book_id': fields.String(required=True),
    'user_id': fields.String(required=True)
})

borrowing_request_model = ns_users.model('BorrowRequest', {
>>>>>>> b3debb05987147f8ccaf8d884e04105f1827165a
    'book_id': fields.String(required=True)
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
        
<<<<<<< HEAD
        items = list(User.objects(id__gt=after_id).order_by('id').limit(limit) if after_id else User.objects().order_by('id').limit(limit))
=======
        items = User.objects(id__gt=after_id).order_by('id').limit(limit) if after_id else User.objects().order_by('id').limit(limit)
>>>>>>> b3debb05987147f8ccaf8d884e04105f1827165a
        pagination = {
            "type": "cursor-based",
            "links": {
                "cur": f"?after={after_id}&limit={limit}",
<<<<<<< HEAD
                "next": f"?after={items[-1].id}&limit={limit}" if len(items) == limit else None
            }
        }
        return wrap_with_metadata_v2(items, user_model, pagination), 200
=======
                "next": f"?after={items[limit - 1].id}&limit={limit}" if len(items) == limit else None
            }
        }
        return wrap_with_metadata_v2(list(items), user_model, pagination), 200
>>>>>>> b3debb05987147f8ccaf8d884e04105f1827165a
    
@ns_users.route('/<string:user_id>')
class UserEntry(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get a specific user"""
        user = User.objects.get(id=user_id)
        
        return wrap_with_metadata_v2(user, user_model), 200

<<<<<<< HEAD
@ns_users.route('/<string:user_id>/borrowings')
class UserBorrows(Resource):
    @jwt_required()
    def get(self, user_id):
        """View list of borrowed books"""
        items = Borrowing.objects(user = user_id).select_related()
        return wrap_with_metadata_v2(list(items), borrowing_model), 200

    @jwt_required()
    @ns_users.expect(borrowing_request_model)
    def post(self, user_id):
        """Borrow a book"""
        data = request.json
        book_id = data.get('book_id')
        
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        
        new_borrowing = Borrowing(user=user.id, book=book.id)
        new_borrowing.save()
        return wrap_with_metadata_v2(new_borrowing, borrowing_model), 201
=======
# @ns_users.route('/<int:user_id>/borrows')
# class UserBorrows(Resource):
#     @jwt_required()
#     def get(self, user_id):
#         """View list of borrowed books"""
#         user_borrows = [b for b in borrows_db if b['user_id'] == user_id]
        
#         result = []
#         # Replicate JOIN statement
#         for b in user_borrows:
#             book = next((book for book in books_db if book['id'] == b['book_id']), None)
#             book["borrow_date"] = b["borrow_date"]
#             result.append(book)
#         return wrap_with_metadata(result), 200

#     @jwt_required()
#     @ns_users.expect(borrow_request_model)
#     def post(self, user_id):
#         """Borrow a book"""
#         data = request.json
#         book_id = data.get('book_id')
        
#         book = next((b for b in books_db if b['id'] == book_id), None)
#         user = next((u for u in users_db if u['id'] == user_id), None)
#         if not book:
#             return wrap_with_metadata_error("book-not-found"), 404
#         if not user:
#             return wrap_with_metadata_error("user-not-found"), 404
        
#         new_borrow = {
#             "user_id": user_id,
#             "book_id": book_id,
#             "borrow_date": datetime.now().isoformat()
#         }
#         borrows_db.append(new_borrow)
#         return wrap_with_metadata(new_borrow), 201
>>>>>>> b3debb05987147f8ccaf8d884e04105f1827165a
