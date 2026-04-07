from werkzeug.security import generate_password_hash, check_password_hash
from models import Book, User, Borrowing

books_db = [
    {"id": 1, "title": "the art of war", "author": "sun tzu", "year": 450},
    {"id": 2, "title": "the c programming language", "author": "brian kernighan", "year": 1978},
    {"id": 3, "title": "test test test", "author": "gaben, icefrog", "year": 2026}
]

users_db = [
    {"id": 1, "username": "admin", "name": "admin"},
    {"id": 2, "username": "trung", "name": "Do Nam Trung"},
    {"id": 3, "username": "gaben", "name": "Gabe Newell"}
]

# ManyToMany relationship
borrows_db = [
    {"user_id": 2, "book_id": 1, "borrow_date": "2026-03-23T10:00:00"}
]

auths_db = []

def init_db():
    # book = Book.objects.first()
    # user = Book.objects.first()
    # borrowing = Borrowing(user=user.id, book=book.id)
    # borrowing.save()
    
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
    