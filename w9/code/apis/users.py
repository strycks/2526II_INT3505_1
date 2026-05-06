from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields, Resource
from utils import cursor_pagination_parser, wrap_with_metadata_v2, role_required
from models import User, Book, Borrowing, AuthAccount
from apis.v2.books import book_model

ns_users = Namespace('users', description='User Management')

user_model = ns_users.model('User', {
    'id': fields.String(required=True),
    'username': fields.String(required=True),
    'name': fields.String(required=True)
})

borrowing_model = ns_users.model('Borrowing', {
    'book': fields.Nested(book_model),
})

borrowing_request_model = ns_users.model('BorrowingRequest', {
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
        
        items = list(User.objects(id__gt=after_id).order_by('id').limit(limit) if after_id else User.objects().order_by('id').limit(limit))
        pagination = {
            "type": "cursor-based",
            "links": {
                "cur": f"?after={after_id}&limit={limit}",
                "next": f"?after={items[-1].id}&limit={limit}" if len(items) == limit else None
            }
        }
        return wrap_with_metadata_v2(items, user_model, pagination), 200
    
@ns_users.route('/<string:user_id>')
class UserEntry(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get a specific user"""
        user = User.objects.get(id=user_id)
        
        return wrap_with_metadata_v2(user, user_model), 200

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
