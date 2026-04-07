from mongoengine import Document, StringField, IntField, ReferenceField
class Book(Document):
    title = StringField(required=True)
    author = StringField(default="Unknown")
    year = IntField(default=2026)
    meta = {
        'collection': 'books',
        'indexes': ['title']
    }
    
class User(Document):
    username = StringField(required=True)
    name = StringField(required=True)
    meta = {
        'collection': 'users',
        'indexes': ['username']
    }
    
class Borrowing(Document):
    user = ReferenceField('User', required=True)
    book = ReferenceField('Book', required=True)
    meta = {
        'collection': 'borrowings'
    }
    