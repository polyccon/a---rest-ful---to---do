import pytest
import requests
from src.views import *

def test_logout_works_():
    """Test if '/logout' works by logging in, then logout and subsequent call to
        add endpoint returns 401
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
    s.get('http://localhost:8000/logout')
    response = s.post('http://localhost:8000/add',
                             json=body2)

    actual = response.status_code

    assert actual == 401
