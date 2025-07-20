import pytest
from flask import Flask
from src.routes.users import users_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_add_user()


