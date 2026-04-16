import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.borrowing_request import BorrowingRequest  # noqa: E501
from openapi_server import util


def get_user_borrows(user_id):  # noqa: E501
    """View list of borrowed books

     # noqa: E501

    :param user_id: 
    :type user_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_user_entry(user_id):  # noqa: E501
    """Get a specific user

     # noqa: E501

    :param user_id: 
    :type user_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_user_list(after=None, limit=None):  # noqa: E501
    """Get all users

     # noqa: E501

    :param after: After index
    :type after: str
    :param limit: Item limit
    :type limit: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def post_user_borrows(user_id, body):  # noqa: E501
    """Borrow a book

     # noqa: E501

    :param user_id: 
    :type user_id: str
    :param payload: 
    :type payload: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    payload = body
    if connexion.request.is_json:
        payload = BorrowingRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
