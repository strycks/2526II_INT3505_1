import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server import util


def delete_book_item(book_id):  # noqa: E501
    """Delete a specific book

     # noqa: E501

    :param book_id: 
    :type book_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_book_item(book_id):  # noqa: E501
    """Get a specific book

     # noqa: E501

    :param book_id: 
    :type book_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_book_list():  # noqa: E501
    """Get all books

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def post_book_list(body):  # noqa: E501
    """Add new book

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    payload = body
    if connexion.request.is_json:
        payload = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
