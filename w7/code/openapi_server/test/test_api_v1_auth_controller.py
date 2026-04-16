import unittest

from flask import json

from openapi_server.models.login import Login  # noqa: E501
from openapi_server.models.register import Register  # noqa: E501
from openapi_server.test import BaseTestCase


class TestApiV1AuthController(BaseTestCase):
    """ApiV1AuthController integration test stubs"""

    def test_post_login(self):
        """Test case for post_login

        Login to get JWT Token
        """
        payload = {"password":"123456","username":"admin"}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/auth/login',
            method='POST',
            headers=headers,
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_refresh(self):
        """Test case for post_refresh

        Refresh token
        """
        headers = { 
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/auth/refresh',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_register(self):
        """Test case for post_register

        Register an user
        """
        payload = {"password":"password","role":"role","name":"name","username":"username"}
        headers = { 
            'Content-Type': 'application/json',
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/auth/register',
            method='POST',
            headers=headers,
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
