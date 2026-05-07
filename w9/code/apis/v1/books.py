from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields, Namespace
from utils import wrap_with_metadata, wrap_with_metadata_error, pagination_parser, role_required, wrap_with_metadata_v2
from models import Book
from utils import deprecated_warning

ns_books = Namespace('books', description='Book Management')

book_model = ns_books.model('Book', {
    'id': fields.String(required=True),
    'title': fields.String(required=True),
    'author': fields.String(default="valve, icefrog"),
    'year': fields.Integer(default=2026)
})

book_request_model = ns_books.model('BookRequest', {
    'title': fields.String(required=True),
    'author': fields.String(default="valve, icefrog"),
    'year': fields.Integer(default=2026)
})

@ns_books.route('')
class BookList(Resource):
    @jwt_required()
    # @ns_books.expect(pagination_parser, validate=True)
    @deprecated_warning("31-12-2026", "/api/v2/books")
    @ns_books.doc(deprecated=True)
    def get(self):
        """Get all books"""
        # args = pagination_parser.parse_args()
        # page = args['page']
        # per_page = args['per_page']
        # query = args.get('q')
        
        # filtered_books = Book.objects.all() if not query else Book.objects(title__icontains=query)
        # total_elements = len(filtered_books)

        # # page = ceil(ele / per)
        # total_pages = (total_elements + per_page - 1) // per_page if total_elements > 0 else 0
        # if page > total_pages and total_pages > 0:
        #     page = total_pages
        
        # start = (page - 1) * per_page
        # end = min(start + per_page, total_elements)
        # items = filtered_books[start:end]

        # pagination = {
        #     "type": "page-based",
        #     "current_page": page,
        #     "per_page": per_page,
        #     "total_elements": total_elements,
        #     "total_pages": total_pages,
        #     "links": {
        #         "next": f"?page={page+1}&per_page={per_page}" + (f"&q={query}" if query != None else "") if page < total_pages else None,
        #         "prev": f"?page={page-1}&per_page={per_page}" + (f"&q={query}" if query != None else "") if page > 1 else None
        #     }
        # }
        items = Book.objects.all()
        return wrap_with_metadata_v2(list(items), book_model)

    @role_required("admin")
    @jwt_required()
    @ns_books.expect(book_request_model, validate=True)
    @ns_books.response(201, 'Created')
    @ns_books.response(400, 'Bad Request')
    def post(self):
        """Add new book"""
        data = request.json
        
        new_book = Book(title = data['title'], author = data.get('author', "Unknown"), year = data.get('year', 2026))
        new_book.save()
        
        return wrap_with_metadata_v2(new_book, book_model), 201

@ns_books.route('/<string:book_id>')
class BookItem(Resource):
    @jwt_required()
    def get(self, book_id):
        """Get a specific book"""
        book = Book.objects.get(id=book_id)
        
        return wrap_with_metadata_v2(book, book_model), 200
    
    @jwt_required()
    @ns_books.response(204, "Deleted")
    def delete(self, book_id):
        """Delete a specific book"""
        book = Book.objects.get(id=book_id)
        book.delete()
        
        return wrap_with_metadata(""), 204