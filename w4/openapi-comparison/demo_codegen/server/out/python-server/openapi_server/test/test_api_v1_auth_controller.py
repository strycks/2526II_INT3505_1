import unittest

from flask import json

from openapi_server.models.login import Login  # noqa: E501
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


if __name__ == '__main__':
    unittest.main()
