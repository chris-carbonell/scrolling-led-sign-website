# Dependencies

# testing
import pytest

# general
import requests

# constants
from . import *

def test_health_check_exists():
    '''
    GIVEN   no params
    WHEN    healthcheck endpoint is called
    THEN    a 200 response should be received
    '''
    res = requests.get(BASE_URL + "healthcheck")
    assert res.status_code == 200