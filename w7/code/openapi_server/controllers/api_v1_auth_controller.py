import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.login import Login  # noqa: E501
from openapi_server.models.register import Register  # noqa: E501
from openapi_server import util


def post_login(body):  # noqa: E501
    """Login to get JWT Token

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    payload = body
    if connexion.request.is_json:
        payload = Login.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_refresh():  # noqa: E501
    """Refresh token

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def post_register(body):  # noqa: E501
    """Register an user

     # noqa: E501

    :param payload: 
    :type payload: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    payload = body
    if connexion.request.is_json:
        payload = Register.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
