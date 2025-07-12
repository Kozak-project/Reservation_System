import pytest
from flask import Flask
from routes.rooms import rooms_bp
from models import Room

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(rooms_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_rooms(client, mocker):
    mock_rooms = [
        Room(room_number=101, price_per_night=150.0),
        Room(room_number=102, price_per_night=200.0),
    ]

    mocker.patch('routes.rooms.all_rooms', return_value=mock_rooms)

    response = client.get('/rooms/all_rooms')

    assert response.status_code == 200
    data = response.get_json()
    assert data == {
        "101": {"price_per_night": 150.0},
        "102": {"price_per_night": 200.0}
    }