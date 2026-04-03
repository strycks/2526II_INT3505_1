import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.patch_books_id_request import PATCHBooksIdRequest  # noqa: E501
from openapi_server import util


def d_elete_books_id(id):  # noqa: E501
    """d_elete_books_id

    Remove a book # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def g_et_books():  # noqa: E501
    """g_et_books

    Get all books # noqa: E501


    :rtype: Union[List[Book], Tuple[List[Book], int], Tuple[List[Book], int, Dict[str, str]]
    """
    return 'do some magic!'


def g_et_books_id(id):  # noqa: E501
    """g_et_books_id

    Get book details # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    return 'do some magic!'


def p_atch_books_id(id, body):  # noqa: E501
    """p_atch_books_id

    Update book fields # noqa: E501

    :param id: 
    :type id: str
    :param patch_books_id_request: 
    :type patch_books_id_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    patch_books_id_request = body
    if connexion.request.is_json:
        patch_books_id_request = PATCHBooksIdRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def p_ost_books(body):  # noqa: E501
    """p_ost_books

    Create a new book # noqa: E501

    :param book: 
    :type book: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book = body
    if connexion.request.is_json:
        book = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def p_ut_books_id(id, body):  # noqa: E501
    """p_ut_books_id

    Replace a book # noqa: E501

    :param id: 
    :type id: str
    :param book: 
    :type book: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book = body
    if connexion.request.is_json:
        book = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
