import unittest

from flask import json

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.book_request import BookRequest  # noqa: E501
from openapi_server.models.login_request import LoginRequest  # noqa: E501
from openapi_server.models.login_response import LoginResponse  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_openapi_server_controllers_auth_controller_login(self):
        """Test case for openapi_server_controllers_auth_controller_login

        User Login
        """
        login_request = {"password":"password","username":"username"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/auth/login',
            method='POST',
            headers=headers,
            data=json.dumps(login_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_openapi_server_controllers_book_controller_create_book(self):
        """Test case for openapi_server_controllers_book_controller_create_book

        Add a new book
        """
        book_request = {"quantity":0,"author":"author","title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/books',
            method='POST',
            headers=headers,
            data=json.dumps(book_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_openapi_server_controllers_book_controller_delete_book(self):
        """Test case for openapi_server_controllers_book_controller_delete_book

        Remove a book
        """
        headers = { 
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id='book_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_openapi_server_controllers_book_controller_get_book_by_id(self):
        """Test case for openapi_server_controllers_book_controller_get_book_by_id

        Get book details
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id='book_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_openapi_server_controllers_book_controller_get_books(self):
        """Test case for openapi_server_controllers_book_controller_get_books

        Get all books
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

    def test_openapi_server_controllers_book_controller_update_book(self):
        """Test case for openapi_server_controllers_book_controller_update_book

        Update a book
        """
        book_request = {"quantity":0,"author":"author","title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/v1/books/{book_id}'.format(book_id='book_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(book_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
