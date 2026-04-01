from flask import request
from flask_restx import Namespace, fields, Resource
from utils import wrap_with_metadata, wrap_with_metadata_error
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from database import auths_db
from datetime import timedelta

ns_auth = Namespace('api/v1/auth', description='Authorization')

login_model = ns_auth.model('Login', {
    'username': fields.String(required=True, default='admin'),
    'password': fields.String(required=True, default='123456')
})

@ns_auth.route('/login')
class Login(Resource):
    @ns_auth.expect(login_model)
    @ns_auth.doc(security=[])
    def post(self):
        """Login to get JWT Token"""
        data = request.json
        username = data.get("username")
        password = data.get("password")
        
        obj = next((u for u in auths_db if u['username'] == username), None)
        
        if not check_password_hash(obj["password"], password):
            return wrap_with_metadata_error("invalid-credentials"), 401

        access_token = create_access_token(identity=username, additional_claims={"role":obj["role"]}, expires_delta=timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=username, expires_delta=timedelta(days=30))
        return wrap_with_metadata({
                "access-token": access_token,
                "refresh_token": refresh_token
            }), 200
        
@ns_auth.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh token"""
        identity = get_jwt_identity()
        user = next((u for u in auths_db if u["username"] == identity), None)
        if not user:
            return wrap_with_metadata_error("refresh-token-not-valid"), 400
        access_token = create_access_token(identity=identity, additional_claims={"role": user['role']})
        return wrap_with_metadata({
            "access_token": access_token
        }), 201
        