from datetime import datetime
from flask_restx import marshal, reqparse
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

def wrap_with_metadata(data, pagination = None):
    response = {
        "metadata": {
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
            "timestamp": datetime.now().isoformat()
        },
        "message": error
    }

def wrap_with_metadata_v2(data, model = None, pagination = None):
    new_data = marshal(data, model) if model else data
    response = {
        "metadata": {
            "timestamp": datetime.now().isoformat()
        },
        "data": new_data
    }
    if pagination:
       response["metadata"]["pagination"] = pagination 
    return response

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
                return wrap_with_metadata_error("Forbidden"), 403

        return decorator

    return wrapper
    
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, default=1, help='Page number')
pagination_parser.add_argument('per_page', type=int, default=10, help='Item per page')
pagination_parser.add_argument('q', type=str, help='Search query')

cursor_pagination_parser = reqparse.RequestParser()
cursor_pagination_parser.add_argument('after', type=str, help='After index')
cursor_pagination_parser.add_argument('limit', type=int, default=10, help='Item limit')