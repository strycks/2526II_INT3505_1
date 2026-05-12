from datetime import datetime
from flask import Blueprint
from flask_restx import Api
from apis.auth import ns_auth
from apis.v1.books import ns_books as ns_books_1
from apis.v2.books import ns_books as ns_books_2
from apis.users import ns_users
from apis.handlers import register_error_handlers

authorizations = {
    "bearerAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

blueprint_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v1 = Api(
    blueprint_v1,
    version='1.0',
    title='Book Management API',
    authorizations=authorizations,
    security='bearerAuth',
    doc='/docs/'
)

api_v1.add_namespace(ns_auth, path='/auth')
api_v1.add_namespace(ns_books_1, path='/books')
api_v1.add_namespace(ns_users, path='/users')
register_error_handlers(api_v1)

blueprint_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api_v2 = Api(
    blueprint_v2,
    version='2.0',
    title='Book Management API',
    authorizations=authorizations,
    security='bearerAuth',
    doc='/docs/'
)

api_v2.add_namespace(ns_auth, path='/auth')
api_v2.add_namespace(ns_books_2, path='/books')
api_v2.add_namespace(ns_users, path='/users')
register_error_handlers(api_v2)


# api = Api(
#     version='1.0', 
#     title='Book Management API',
#     authorizations=authorizations,
#     security='bearerAuth',
#     doc='/apidocs/'
# )

# register_error_handlers(api)
# api.add_namespace(ns_auth)
# api.add_namespace(ns_books)
# api.add_namespace(ns_users)