import pytest
from flask import Flask
from src.routes.rooms import rooms_bp
from src.models import Room


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(rooms_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_add_room(client, mocker):
    mock_session = mocker.Mock()
    mocker.patch('src.routes.rooms.SessionLocal', return_value=mock_session)


    response = client.post('/rooms/add_room', json={
        'room_number': 201,
        'price_per_night': 150.00
    })

    assert response.status_code == 201
    assert response.get_json()['message'] == 'Room added successfully'
    mock_session.add.assert_called()
    mock_session.commit.assert_called()
    mock_session.close.assert_called()


def test_get_all_rooms(client, mocker):
    mock_rooms = [
        Room(room_number=101, price_per_night=150.0),
        Room(room_number=102, price_per_night=200.0),
    ]

    mocker.patch('src.routes.rooms.all_rooms', return_value=mock_rooms)

    response = client.get('/rooms/all_rooms')

    assert response.status_code == 200
    data = response.get_json()
    assert data == {
        "101": {"price_per_night": 150.0},
        "102": {"price_per_night": 200.0}
    }


def test_get_available_rooms(client, mocker):
    mock_rooms = [
        Room(room_number=101, price_per_night=150.0),
        Room(room_number=102, price_per_night=200.0),
    ]

    mocker.patch('src.routes.rooms.all_rooms', return_value=mock_rooms)

    response = client.get('/rooms/available_rooms')

    assert response.status_code == 200
    data = response.get_json()
    assert data == {
        "101": {"price_per_night": 150.0},
        "102": {"price_per_night": 200.0}
    }