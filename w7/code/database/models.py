from mongoengine import Document, StringField, IntField, ReferenceField

class Book(Document):
    title = StringField(required=True)
    author = StringField()
    quantity = IntField(default=1)
    meta = {'collection': 'books'}

class Auth(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)  # Store Hashed Password
    meta = {'collection': 'auths'}