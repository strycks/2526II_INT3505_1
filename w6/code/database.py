from werkzeug.security import generate_password_hash

auths_db = []

def init_db():
    
    auths_db.append({
        "id": 1,
        "username": "admin",
        "password": generate_password_hash("123456"),
        "role": "admin"
    })
    auths_db.append({
        "id": 2,
        "username": "gaben",
        "password": generate_password_hash("nerfmeepopls"),
        "role": "user"
    })
    