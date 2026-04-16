from database.models import Auth
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash
from datetime import timedelta

def authenticate(user_details):
    data = user_details.to_dict()
    username = data.get("username")
    password = data.get("password")

    usr = Auth.objects.get(username=username)
    
    if not check_password_hash(usr.password, password):
        return None

    access_token = create_access_token(
        identity=username, 
        expires_delta=timedelta(minutes=15)
    )
    refresh_token = create_refresh_token(
        identity=username, 
        expires_delta=timedelta(days=30)
    )
    return {
            "access-token": access_token,
            "refresh_token": refresh_token
        }