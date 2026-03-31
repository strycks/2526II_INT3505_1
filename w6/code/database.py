from werkzeug.security import generate_password_hash, check_password_hash

books_db = [
    {"id": 1, "title": "the art of war", "author": "sun tzu", "year": 450},
    {"id": 2, "title": "the c programming language", "author": "brian kernighan", "year": 1978}
]

users_db = [
    {"id": 1, "username": "admin", "name": "admin"},
    {"id": 2, "username": "trung", "name": "Do Nam Trung"},
    {"id": 3, "username": "mixi", "name": "Phung Thanh Do"}
]

# ManyToMany relationship
borrows_db = [
    {"user_id": 2, "book_id": 1, "borrow_date": "2026-03-23T10:00:00"}
]

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
        "username": "mixi",
        "password": generate_password_hash("camonanhanhdomixi"),
        "role": "user"
    })
    