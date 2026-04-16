#!/usr/bin/env python3

import connexion
from dotenv import load_dotenv
from mongoengine import connect
from flask_jwt_extended import JWTManager
import os
from database.utils import create_admin

from openapi_server import encoder


def main():
    load_dotenv()
    connect(host=os.getenv("MONGODB_URI"))
    
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder  
    app.add_api('openapi.yaml',
                arguments={'title': 'Simplified Library Management API'},
                pythonic_params=True)

    app.app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
    JWTManager(app.app)
    
    create_admin()

    app.run(port=8080)


if __name__ == '__main__':
    main()
