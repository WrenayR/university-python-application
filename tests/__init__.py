import pytest
from app import app as flask_app
from app import *


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['LOGIN_DISABLED'] = True
    flask_app.app_context().push()
    db.create_all()
    client = flask_app.test_client()
    return client
