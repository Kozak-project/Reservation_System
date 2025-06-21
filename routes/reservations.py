from flask import Blueprint, jsonify, request
from models import Reservation, User, Room
from database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


reservations_bp = Blueprint('reservation', __name__, url_prefix='/reservation')


@reservations_bp.route('/add', methods=['POST'])
def add_reservation():
    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Data is None'})

    user_id = data['user_id']
    last_name = data['last_name']
    email = data['email']
    phone_number = data['phone_number']
    room_id = data['room_id']
    start_time = datetime.fromisoformat(data['start_time'])
    end_time = datetime.fromisoformat(data['end_time'])

    session = SessionLocal()
    try:
        conflicting = session.query(Reservation).filter(
            Reservation.room_id == room_id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time
        ).first()
        if conflicting:
            return jsonify({'Error': f'Room ID: {room_id} is already booked in this range time'})

        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
        else:
            user = User(last_name=last_name, email=email, phone_number=phone_number)
            session.add(user)
            session.flush()

        reservation = Reservation(user_id=user.id, room_id=room_id, start_time=start_time, end_time=end_time)

        session.add(reservation)
        session.commit()
        return jsonify({'Success': 'Reservation has been added'}), 201
    except SQLAlchemyError:
        session.rollback()
        return jsonify({'Error': 'Database error'}), 500
    finally:
        session.close()


@reservations_bp.route('/find_user/<int:user_id>/')
def user_reservations(user_id):
    session = SessionLocal()
    try:
        user_reservation = session.query(Reservation).filter(Reservation.user_id == user_id).all()
        if not user_reservation:
            return jsonify({'message': f'User: {user_id} does not have reservations or does not exist'}), 404

        result = [
            {
                'Room ID': reservation.room_id,
                'Booked from:': reservation.start_time.isoformat(),
                'Booked to': reservation.end_time.isoformat()
            }
            for reservation in user_reservation
        ]
        return jsonify(result), 200

    except SQLAlchemyError:
        session.rollback()
        return jsonify({'Error': 'Database error'}), 500
    finally:
        session.close()


@reservations_bp.route('/update/<int:reservation_id>/', methods=['PUT'])
def edit_reservation_time(reservation_id):
    data = request.get_json()
    start_time = datetime.fromisoformat(data['start_time'])
    end_time = datetime.fromisoformat(data['end_time'])

    session = SessionLocal()
    try:
        reservation = session.query(Reservation).filter(Reservation.id == reservation_id).first()
        if reservation:
            reservation.start_time = start_time
            reservation.end_time = end_time
        else:
            return jsonify({'Error': 'reservation not found'}), 404

        session.commit()
        return jsonify({'Success': 'Reservation has been updated'}), 200
    except SQLAlchemyError:
        session.rollback()
        return jsonify({'Error': 'Database error'}), 500
    finally:
        session.close()


@reservations_bp.route('/delete/<int:reservation_id>/', methods=['DELETE'])
def delete_reservation(reservation_id):
    session = SessionLocal()

    try:
        reservation = session.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            return jsonify({'Error': f'Reservation: {reservation_id} not found'}), 404

        session.delete(reservation)
        session.commit()
        return jsonify({'Success': f'Reservation: {reservation_id} has been deleted'}), 200
    except SQLAlchemyError:
        session.rollback()
        return jsonify({'Error': 'Database error'}), 500
    finally:
        session.close()
