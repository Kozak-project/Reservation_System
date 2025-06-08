from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify, request
from models import Room
from database import SessionLocal


rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')


@rooms_bp.route('/add_room', methods=['POST'])
def add_room():
    session = SessionLocal()
    try:
        data = request.get_json()
        room_number = data['room_number']
        price_per_night = data['price_per_night']
        is_reserved = data['is_reserved']
        room = Room(room_number=room_number, price_per_night=price_per_night, is_reserved=is_reserved)
        session.add(room)
        session.commit()
        return jsonify({'message': 'Room added successfully'}), 201
    except SQLAlchemyError as e:
        session.rollback()
        print(f'Database error: {e}')
        return jsonify({'error': 'Database error'})
    finally:
        session.close()


@rooms_bp.route('/available_rooms')
def get_rooms():
    try:
        with SessionLocal() as session:
            rooms = session.query(Room).all()
            available_rooms = [room.room_number for room in rooms if not room.is_reserved]
            return jsonify(available_rooms), 200
    except SQLAlchemyError as e:
        print(f'Database Error: {e}')
        return jsonify({'Error': 'Database error'}), 500
