import pytest
import requests
from src.views import *

def test_delete_a_todo():
    """Test if '/login' and subsequent call to '/delete' endpoint returns 200
        when auth details are correct
    """
    body1 = {
        'username': 'Dustin Hoffman',
        'password': 'Rainman'
    }
    body2 = {
        'task': 'ironing and cleaning'
    }
    s = requests.session()

    s.post('http://localhost:8000/todos/login',
                             json=body1)
    s.post('http://localhost:8000/todos',
                             json=body2)
    response = s.delete('http://localhost:8000/todos/1/delete',
                             json=body2)

    actual = response.json()['tasks']
    assert actual == []

    actual_status_code = response.status_code
    assert actual_status_code == 200
