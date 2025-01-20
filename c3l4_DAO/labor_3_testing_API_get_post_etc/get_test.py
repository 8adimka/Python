import pytest
from get_search import app


def test_all():
    params = {"s": "python"}
    response = app.test_client().get('/search/', query_string=params)
    print(response.json)
    assert response.status_code == 200
    assert len(response.json) == 3

def test_one():
    params = {"s": "новичков"}
    response = app.test_client().get('/search/', query_string=params)
    print(response.json)
    assert response.status_code == 200
    assert len(response.json) == 1

def test_none():
    params = {"s": "java"}
    response = app.test_client().get('/search/', query_string=params)
    print(response.json)
    assert response.status_code == 200
    assert len(response.json) == 0
