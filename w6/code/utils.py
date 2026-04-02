from datetime import datetime
from flask_restx import reqparse
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
import base64

def wrap_with_metadata(data, pagination = None):
    response = {
        "metadata": {
            "apiVersion": "1.0",
            "timestamp": datetime.now().isoformat()
        },
        "data": data
    }
    if pagination:
       response["metadata"]["pagination"] = pagination 
    return response

def wrap_with_metadata_error(error):
    return {
        "metadata": {
            "apiVersion": "1.0",
            "timestamp": datetime.now().isoformat()
        },
        "error": error
    }

def role_required(roles):
    if isinstance(roles, str):
        roles = [roles]
    
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] in roles:
                return fn(*args, **kwargs)
            else:
                return wrap_with_metadata_error("forbidden"), 403

        return decorator

    return wrapper
    
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, default=1, help='Page number')
pagination_parser.add_argument('per_page', type=int, default=10, help='Item per page')
pagination_parser.add_argument('q', type=str, help='Search query')

cursor_pagination_parser = reqparse.RequestParser()
cursor_pagination_parser.add_argument('after', type=int, default=1, help='After index')
cursor_pagination_parser.add_argument('limit', type=int, default=10, help='Item limit')