import unittest

from flask import json

from openapi_server.models.book_request import BookRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestApiV1BooksController(BaseTestCase):
    """ApiV1BooksController integration test stubs"""

    def test_delete_book_item(self):
        """Test case for delete_book_item

        Delete a specific book
        """
        headers = { 
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id='book_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_book_item(self):
        """Test case for get_book_item

        Get a specific book
        """
        headers = { 
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id='book_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_book_list(self):
        """Test case for get_book_list

        Get all books
        """
        query_string = [('page', 1),
                        ('per_page', 10),
                        ('q', 'q_example')]
        headers = { 
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/books',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_book_list(self):
        """Test case for post_book_list

        Add new book
        """
        payload = {"year":0,"author":"valve, icefrog","title":"title"}
        headers = { 
            'Content-Type': 'application/json',
            'bearerAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v1/books',
            method='POST',
            headers=headers,
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
