import pytest
from flask import session

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Homepage - CS235 Flix' in response.data

def test_movies_list(client):
    # Check that we can retrieve the movies list page.
    response = client.get('/list?page_num=1')
    assert response.status_code == 200
    assert b'Page 1 - Movie List - CS235 Flix' in response.data

def test_movies_list_no_number(client):
    # Check that we can redirect to the first page of the movies list if no number is provided.
    response = client.get('/list/')
    assert response.status_code == 302
    assert b'Redirecting...' in response.data

def test_movies_list_zero_number(client):
    # Check that we can redirect to the first page of the movies list if 0 is provided.
    response = client.get('/list?page_num=0')
    assert response.status_code == 302
    assert b'Redirecting...' in response.data

def test_movies_list_negative_number(client):
    # Check that we can redirect to the first page of the movies list if a negative number is provided.
    response = client.get('/list/?page_num=-10')
    assert response.status_code == 302
    assert b'Redirecting...' in response.data

def test_movies_list_index_out_of_bounds(client):
    # Check that we can redirect to the first page of the movies list if page is provided.
    # Note that there are 15 movies per page, so with 1000 movies, there's a maximum of 67 pages
    response = client.get('/list/?page_num=100')
    assert response.status_code == 302
    assert b'Redirecting...' in response.data
