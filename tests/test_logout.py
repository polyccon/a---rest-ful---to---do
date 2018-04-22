import pytest
import requests
from src.views import *

def test_logout_endpoint():
    """Test if '/logout' works by logging in, then logout and subsequent call to
        add endpoint returns 401
    """
    body1 = {
        'username': 'user18081971',
        'password': 'Aphex'
    }
    body2 = {
        'todo': 'clean my cds'
    }
    s = requests.session()

    s.post('http://localhost:8000/session',
                             json=body1)
    s.delete('http://localhost:8000/session')
    response = s.post('http://localhost:8000/todos',
                             json=body2)

    actual = response.json()
    actual_status_code = response.status_code
    assert actual_status_code == 401
    assert actual['message'] == 'Login required'
    assert actual['error'] == True
