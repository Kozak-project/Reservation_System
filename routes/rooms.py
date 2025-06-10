from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify, request
from models import Room
from database import SessionLocal


rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')


def all_rooms():
    with SessionLocal() as session:
        rooms = session.query(Room).all()

        return rooms


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
    except SQLAlchemyError:
        session.rollback()
        return jsonify({'error': 'Database error'})
    finally:
        session.close()


@rooms_bp.route('/all_rooms')
def get_all_rooms():
    try:
        rooms = all_rooms()
        all_rooms_details = {}
        for room in rooms:
            all_rooms_details[room.room_number] = {'price_per_night': float(room.price_per_night),
                                                   'is_reserved': room.is_reserved,
                                                   'reserved_by': room.reserved_by,
                                                   'start_time': room.start_time and room.start_time.isoformat(),
                                                   'end_time': room.end_time and room.end_time.isoformat()}
        return jsonify(all_rooms_details)
    except SQLAlchemyError:
        return jsonify({'error': 'Database error'}), 500


@rooms_bp.route('/available_rooms')
def get_available_rooms():
    try:
        rooms = all_rooms()
        available_rooms = {}
        for room in rooms:
            if not room.is_reserved:
                available_rooms[room.room_number] = room.price_per_night

        return jsonify(available_rooms)
    except SQLAlchemyError:
        return jsonify({'Error': 'Database error'}), 500


@rooms_bp.route('/delete_room/<int:room_id>/', methods=['DELETE'])
def delete_room(room_id):
    session = SessionLocal()
    try:
        room = session.query(Room).filter(Room.id == room_id).first()
        if room:
            session.delete(room)
            session.commit()
            return jsonify({'message': f'Room with ID: {room_id} deleted successfully'}), 200
        else:
            return jsonify({'message': f'Room with ID: {room_id} not found'}), 404
    except SQLAlchemyError:
        session.rollback()
        return jsonify({'message': 'Database error'}), 500
    finally:
        session.close()
