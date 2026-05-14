from flask import request
from flask_restx import Namespace, fields, Resource
from utils import wrap_with_metadata, wrap_with_metadata_error, wrap_with_metadata_v2
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from models import AuthAccount, User
from apis.users import user_model

ns_auth = Namespace('api/v1/auth', description='Authorization')

login_model = ns_auth.model('Login', {
    'username': fields.String(required=True, default='admin'),
    'password': fields.String(required=True, default='123456')
})

register_model = ns_auth.model('Register', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'name': fields.String(required=True),
    'role': fields.String()
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
    
        usr = AuthAccount.objects.get(username=username)
        
        if not check_password_hash(usr.password, password):
            return wrap_with_metadata_error("Invalid credentials"), 401

        access_token = create_access_token(
            identity=username, 
            additional_claims={"role":usr.role}, 
            expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_refresh_token(
            identity=username, 
            expires_delta=timedelta(days=30)
        )
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
        user = AuthAccount.objects(username=identity).first()
        if not user:
            return wrap_with_metadata_error("Invalid refresh token"), 401
        access_token = create_access_token(
            identity=identity, 
            additional_claims={"role": user.role}
        )
        return wrap_with_metadata({
            "access_token": access_token
        }), 201
        
@ns_auth.route('/register')
class Register(Resource):
    @ns_auth.expect(register_model)
    def post(self):
        """Register an user"""
        data = ns_auth.payload
        if AuthAccount.objects(username=data['username']).first():
            ns_auth.abort(400, "Username already exists")
        
        new_auth = AuthAccount(
            username=data['username'],
            password=generate_password_hash(data['password'])
        )
        
        if data['role']:
            new_auth.role = data['role']
        new_auth.save()

        new_user = User(
            auth_account=new_auth,
            name=data['name'],
            username=data['username']
        ).save()

        return wrap_with_metadata_v2(new_user, user_model), 201