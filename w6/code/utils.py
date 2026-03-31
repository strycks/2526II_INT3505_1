from datetime import datetime
from flask_restx import reqparse

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
    
pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, default=1, help='Page number')
pagination_parser.add_argument('per_page', type=int, default=10, help='Item per page')
pagination_parser.add_argument('q', type=str, help='Search query')