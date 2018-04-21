import pytest
import requests
from src.views import *

@pytest.mark.parametrize(
    ("params", "expected"),
    [
        (['http://localhost:8000/add',
                                {
                                     'task': 'clean my cds'
                                 }],
        401)
    ]
)
def test_is_equal(params, expected):
    """Test if call to '/add' endpoint is authenticated
    """
    response = requests.session().post(url= params[0], json=params[1])
    actual = response.status_code
    assert actual == expected
