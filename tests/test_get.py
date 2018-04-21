import pytest
import requests
from src.views import *

def test_get_endpoint():
    """Test if '/get' returns tasks and 200 status code when auth details are correct
    """
    body1 = {
        'username': 'Dustin Hoffman',
        'password': 'Rainman'
    }
    s = requests.session()

    s.post('http://localhost:8000/login',
                             json=body1)
    response = s.get('http://localhost:8000/get')

    actual = response.json()['tasks']
    assert actual == []

    actual_status_code = response.status_code
    assert actual_status_code == 200
