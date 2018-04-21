import pytest
import requests
from src.views import *

def test_login_works_and_delete_a_todo_subsequently():
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

    s.post('http://localhost:8000/login',
                             json=body1)
    s.post('http://localhost:8000/add',
                             json=body2)
    response = s.delete('http://localhost:8000/delete/1',
                             json=body2)

    actual = response.json()['tasks']
    actual_status_code = response.status_code
    assert actual_status_code == 200
    assert actual == []
