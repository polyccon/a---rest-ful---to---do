import pytest
import requests
from src.views import *

def test_login_works_and_delete_a_todo_subsequently():
    """Test if '/login' and subsequent call to '/delete' endpoint returns 200
        when auth details are correct
    """
    body1 = {
        'username': 'user18081971',
        'password': 'Aphex'
    }
    body2 = {
        'task': 'clean my cds'
    }
    s = requests.session()

    s.post('http://localhost:8000/login',
                             json=body1)
    response = s.delete('http://localhost:8000/delete/1',
                             json=body2)

    actual = response.status_code

    assert actual == 200
