import pytest
from flaskr import create_app

@pytest.fixture(scope='session', autouse=False)
def app():
    return create_app(True)