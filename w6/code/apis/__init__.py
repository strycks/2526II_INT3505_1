from datetime import datetime
from flask_restx import Api
from apis.auth import ns_auth
from apis.books import ns_books
from apis.users import ns_users
from apis.handlers import register_error_handlers

authorizations = {
    "bearerAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

api = Api(
    version='1.0', 
    title='Book Management API',
    authorizations=authorizations,
    security='bearerAuth',
    doc='/apidocs/'
)

register_error_handlers(api)

api.add_namespace(ns_auth)
api.add_namespace(ns_books)
api.add_namespace(ns_users)