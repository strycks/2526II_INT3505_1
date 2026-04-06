from mongoengine import Document, StringField, IntField
class Book(Document):
    title = StringField(required=True)
    author = StringField(default="Unknown")
    year = IntField(default=2026)
    meta = {
        'collection': 'books',
        'indexes': ['title']
    }