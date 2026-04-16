#!/usr/bin/env python3

import connexion
from dotenv import load_dotenv
from mongoengine import connect
from flask_jwt_extended import JWTManager
import os
from database.utils import create_admin
from mongoengine import ValidationError, DoesNotExist

from openapi_server import encoder

def handle_validation_error(e):
    return {"title": "Resource Validation Error", "details": str(e), "status": 400}, 400

def handle_not_found(e):
    return {"title": "Resource not found", "details": str(e), "status": 404}, 404

def main():
    load_dotenv()
    connect(host=os.getenv("MONGODB_URI"))
    
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder  
    
    app.app.register_error_handler(ValidationError, handle_validation_error)
    app.app.register_error_handler(DoesNotExist, handle_not_found)
    
    app.add_api('openapi.yaml',
                arguments={'title': 'Simplified Library Management API'},
                pythonic_params=True)

    app.app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
    JWTManager(app.app)
    
    create_admin()

    app.run(port=8080)


if __name__ == '__main__':
    main()