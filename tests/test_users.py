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


def test_all_users(client, mocker):
    mock_users = [
        mocker.Mock(id=1, last_name='Sam', phone_number=123456789, email='sam@example.com'),
        mocker.Mock(id=2, last_name='John', phone_number=987654321, email='john@example.com')
    ]

    mock_session = mocker.Mock()
    mock_query = mocker.Mock()
    mock_query.all.return_value = mock_users
    mock_session.query.return_value = mock_query

    mocker.patch('src.routes.users.SessionLocal', return_value=mock_session)

    response = client.get('/user/all_users')

    assert response.status_code == 200
    assert response.json == [
        {
            'user ID': 1,
            'user lastname': 'Sam',
            'user phone number': 123456789,
            'user e-mail': 'sam@example.com'
        },
        {
            'user ID': 2,
            'user lastname': 'John',
            'user phone number': 987654321,
            'user e-mail': 'john@example.com'
        }
    ]
    