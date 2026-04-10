import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.create_book_request import CreateBookRequest  # noqa: E501
from openapi_server.models.partial_update_request import PartialUpdateRequest  # noqa: E501
from openapi_server import util


def create_book(body=None):  # noqa: E501
    """Create Book

     # noqa: E501

    :param create_book_request: 
    :type create_book_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    create_book_request = body
    if connexion.request.is_json:
        create_book_request = CreateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_book(id):  # noqa: E501
    """Delete Book

     # noqa: E501

    :param id: Book ID
    :type id: 

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_book(id):  # noqa: E501
    """Get Book

     # noqa: E501

    :param id: Book ID
    :type id: 

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_all_books():  # noqa: E501
    """List All Books

     # noqa: E501


    :rtype: Union[List[object], Tuple[List[object], int], Tuple[List[object], int, Dict[str, str]]
    """
    return 'do some magic!'


def partial_update(id, body=None):  # noqa: E501
    """Partial Update

     # noqa: E501

    :param id: Book ID
    :type id: 
    :param partial_update_request: 
    :type partial_update_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    partial_update_request = body
    if connexion.request.is_json:
        partial_update_request = PartialUpdateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def replace_book(id, body=None):  # noqa: E501
    """Replace Book

     # noqa: E501

    :param id: Book ID
    :type id: 
    :param create_book_request: 
    :type create_book_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    create_book_request = body
    if connexion.request.is_json:
        create_book_request = CreateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
