from flask_jwt_extended import create_access_token
import pytest
import mongomock
from mongoengine import connect, disconnect

from main import app 
from models import Book

@pytest.fixture
def client():
    disconnect()
    
    connect(
        db='mongoenginetest',
        mongo_client_class=mongomock.MongoClient
    )

    app.config['TESTING'] = True
    
    app.config['JWT_SECRET_KEY'] = 'tXHzZyrglpWqIgfONgcI+gsoCnXKhFFRsFsLtfx0JqU='

    with app.test_client() as client:
        yield client

    disconnect()
    
def test_get_empty_books(client, auth_headers):
    response = client.get('/api/v1/books', headers=auth_headers)
    
    assert response.status_code == 200
    
    data = response.json
    assert isinstance(data.get("data"), list)
    assert len(data.get("data")) == 0

def test_create_book_success(client, auth_headers):
    new_book = {
        "title": "Dota 3",
        "author": "Gaben, Valve"
    }
    
    response = client.post('/api/v1/books', json=new_book, headers=auth_headers)
    
    assert response.status_code == 201
    
    data = response.json
    assert data.get("data")['title'] == "Dota 3"
    
    assert Book.objects.count() == 1

def test_create_book_missing_field(client, auth_headers):
    invalid_book = {
        "author": "No Title Book"
    }
    
    response = client.post('/api/v1/books', json=invalid_book, headers=auth_headers)
    
    assert response.status_code == 400
    assert "Input payload validation failed" in response.json['message']
    
@pytest.fixture
def auth_headers(client):
    with app.app_context():
        access_token = create_access_token(identity='admin', additional_claims={"role":"admin"})
        
    return {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }