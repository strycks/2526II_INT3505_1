from database.models import Book

def get_all_books():
    return list(Book.objects.all())

def get_book_by_id(b_id):
    return Book.objects.get(id=b_id)

def create_new_book(data):
    data = data.to_dict()
    new_book = Book(**data)
    return new_book.save()

def update_existing_book(b_id, data):
    book = Book.objects.get(id=b_id)
    data = data.to_dict()
    if book:
        book.update(**data)
        return book.reload()
    return None

def remove_book(b_id):
    book = Book.objects(id=b_id).first()
    if book:
        book.delete()
        return True
    return False