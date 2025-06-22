from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import User
from database import SessionLocal


users_bp = Blueprint('users', __name__, url_prefix='/user')


@users_bp.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    last_name = data['last_name']
    email = data['email']
    phone_number = data['phone_number']

    session = SessionLocal()
    try:
        user = User(last_name=last_name, email=email, phone_number=phone_number)

        session.add(user)
        session.commit()

        return jsonify({'Success': 'User has been added'}), 201
    except SQLAlchemyError:
        session.rollback()
        return jsonify({'Error': 'Database error'}), 500
    finally:
        session.close()


@users_bp.route('/all_users')
def all_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()

        result = [{'user ID': user.id,
                   'user lastname': user.last_name,
                   'user phone number': user.phone_number,
                   'user e-mail': user.email}
                  for user in users
                  ]

        return jsonify(result), 200
    except SQLAlchemyError:
        session.rollback()
        return jsonify({'Error': 'Database error'}), 500
    finally:
        session.close()


@users_bp.route('/update_user/<int:user_id>/', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    last_name = data['last_name']
    email = data['email']
    phone_number = data['phone_number']

    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()

        if user:
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
        else:
            return jsonify({'Error': 'User not found'}), 404
        session.commit()

        return jsonify({'Success': f'User: {user.last_name} has been updated'}), 200
    except SQLAlchemyError:
        session.rollback()
        return jsonify({'Error', 'Database error'}), 500
    finally:
        session.close()


@users_bp.route('/delete_user/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        session.delete(user)
        session.commit()

        return jsonify({'Success': f'User: {user.last_name} has been deleted'})
    except SQLAlchemyError:
        session.rollback()
        return jsonify({'Error', 'Database error'}), 500
    finally:
        session.close()
        