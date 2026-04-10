import unittest

from flask import json

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.create_book_request import CreateBookRequest  # noqa: E501
from openapi_server.models.partial_update_request import PartialUpdateRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestBooksController(BaseTestCase):
    """BooksController integration test stubs"""

    def test_create_book(self):
        """Test case for create_book

        Create Book
        """
        create_book_request = openapi_server.CreateBookRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books',
            method='POST',
            headers=headers,
            data=json.dumps(create_book_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_book(self):
        """Test case for delete_book

        Delete Book
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_book(self):
        """Test case for get_book

        Get Book
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_all_books(self):
        """Test case for list_all_books

        List All Books
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_partial_update(self):
        """Test case for partial_update

        Partial Update
        """
        partial_update_request = openapi_server.PartialUpdateRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id=1),
            method='PATCH',
            headers=headers,
            data=json.dumps(partial_update_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_replace_book(self):
        """Test case for replace_book

        Replace Book
        """
        create_book_request = openapi_server.CreateBookRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(create_book_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
