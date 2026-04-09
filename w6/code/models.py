from mongoengine import Document, StringField, IntField, ReferenceField, ListField
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
    auth_account = ReferenceField('AuthAccount', required=True)
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
    
class AuthAccount(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    roles = ListField(StringField())
    meta = {
        'collection': 'auth_accounts',
        'indexes': ['username']
    }