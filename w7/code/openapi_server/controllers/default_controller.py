import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.book_request import BookRequest  # noqa: E501
from openapi_server.models.login_request import LoginRequest  # noqa: E501
from openapi_server.models.login_response import LoginResponse  # noqa: E501
from openapi_server import util

from services import book_service, auth_service
from openapi_server.models.book import Book as BookDTO
from database import utils


def openapi_server_controllers_auth_controller_login(body):  # noqa: E501
    """User Login

     # noqa: E501

    :param login_request: 
    :type login_request: dict | bytes

    :rtype: Union[LoginResponse, Tuple[LoginResponse, int], Tuple[LoginResponse, int, Dict[str, str]]
    """
    login_request = body
    if connexion.request.is_json:
        login_request = LoginRequest.from_dict(connexion.request.get_json())  # noqa: E501
    
    tokens = auth_service.authenticate(login_request)
    if not tokens:
        return {"message": "Invalid username or password"}, 401
    return tokens


def openapi_server_controllers_book_controller_create_book(body):  # noqa: E501
    """Add a new book

     # noqa: E501

    :param book_request: 
    :type book_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book_request = body
    if connexion.request.is_json:
        book_request = BookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    
    return utils.convert_mongo(book_service.create_new_book(book_request)), 201


def openapi_server_controllers_book_controller_delete_book(book_id):  # noqa: E501
    """Remove a book

     # noqa: E501

    :param book_id: 
    :type book_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    book_service.remove_book(book_id)
    return '', 204


def openapi_server_controllers_book_controller_get_book_by_id(book_id):  # noqa: E501
    """Get book details

     # noqa: E501

    :param book_id: 
    :type book_id: str

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book = book_service.get_book_by_id(book_id)
    if not book:
        return {"message": "Not found"}, 404
    return utils.convert_mongo(book)


def openapi_server_controllers_book_controller_get_books():  # noqa: E501
    """Get all books

     # noqa: E501


    :rtype: Union[List[Book], Tuple[List[Book], int], Tuple[List[Book], int, Dict[str, str]]
    """
    books = book_service.get_all_books()
    return [utils.convert_mongo(b) for b in books]


def openapi_server_controllers_book_controller_update_book(book_id, body):  # noqa: E501
    """Update a book

     # noqa: E501

    :param book_id: 
    :type book_id: str
    :param book_request: 
    :type book_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book_request = body
    if connexion.request.is_json:
        book_request = BookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    
    book = book_service.update_existing_book(book_id, book_request)
    if not book:
        return {"message": "Not found"}, 404
    return utils.convert_mongo(book)
