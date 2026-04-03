import unittest

from flask import json

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.patch_books_id_request import PATCHBooksIdRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_d_elete_books_id(self):
        """Test case for d_elete_books_id

        
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_g_et_books(self):
        """Test case for g_et_books

        
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

    def test_g_et_books_id(self):
        """Test case for g_et_books_id

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_p_atch_books_id(self):
        """Test case for p_atch_books_id

        
        """
        patch_books_id_request = openapi_server.PATCHBooksIdRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id='id_example'),
            method='PATCH',
            headers=headers,
            data=json.dumps(patch_books_id_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_p_ost_books(self):
        """Test case for p_ost_books

        
        """
        book = {"year":6,"author":"author","id":0,"title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books',
            method='POST',
            headers=headers,
            data=json.dumps(book),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_p_ut_books_id(self):
        """Test case for p_ut_books_id

        
        """
        book = {"year":6,"author":"author","id":0,"title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/books/{id}'.format(id='id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(book),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
