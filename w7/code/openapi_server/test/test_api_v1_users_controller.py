import unittest

from flask import json

from openapi_server.models.borrowing_request import BorrowingRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestApiV1UsersController(BaseTestCase):
    """ApiV1UsersController integration test stubs"""

    def test_get_user_borrows(self):
        """Test case for get_user_borrows

        View list of borrowed books
        """
        headers = { 
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/users/{user_id}/borrowings'.format(user_id='user_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_entry(self):
        """Test case for get_user_entry

        Get a specific user
        """
        headers = { 
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/users/{user_id}'.format(user_id='user_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_list(self):
        """Test case for get_user_list

        Get all users
        """
        query_string = [('after', 'after_example'),
                        ('limit', 10)]
        headers = { 
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/users',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_user_borrows(self):
        """Test case for post_user_borrows

        Borrow a book
        """
        payload = {"book_id":"book_id"}
        headers = { 
            'Content-Type': 'application/json',
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/users/{user_id}/borrowings'.format(user_id='user_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
