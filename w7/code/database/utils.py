from werkzeug.security import generate_password_hash
from database.models import Auth

def convert_mongo(data):
    data = data.to_mongo().to_dict()
    data['id'] = str(data.pop('_id'))
    return data

def create_admin():
    if not Auth.objects(username="admin").first():
        hashed_pw = generate_password_hash("123456")
        Auth(username="admin", password=hashed_pw).save()
        print("Admin user created!")