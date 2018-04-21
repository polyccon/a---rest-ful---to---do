import pytest
import requests
from src.views import *

def test_get_todos_endpoint():
    """Test if '/todos' returns tasks and 200 status code when auth details are correct
    """
    body1 = {
        'username': 'Homer Simpson',
        'password': 'TV'
    }
    s = requests.session()

    s.post('http://localhost:8000/session',
                             json=body1)
    response = s.get('http://localhost:8000/todos')

    actual = response.json()['tasks']
    assert actual == []

    actual_status_code = response.status_code
    assert actual_status_code == 200
