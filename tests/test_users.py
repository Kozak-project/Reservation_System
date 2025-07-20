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


@pytest.mark.parametrize('last_name, email, phone_number', [
    ('Sam', 'sam@example.com', 123456789),
    ('Alex', 'alex@example.com', 987654321)
])
def test_add_user(client, mocker, last_name, email, phone_number):
    mock_session = mocker.Mock()

    mocker.patch('src.routes.users.SessionLocal', return_value=mock_session)

    response = client.post('/user/add', json={
        'last_name': last_name,
        'email': email,
        'phone_number': phone_number
    })

    assert response.status_code == 201
    assert response.get_json()['Success'] == 'User has been added'
    mock_session.add.assert_called()
    mock_session.commit.assert_called()
    mock_session.close.assert_called()
