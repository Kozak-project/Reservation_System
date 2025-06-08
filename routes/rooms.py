from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify
from models import Room
from database import SessionLocal


rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')


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
