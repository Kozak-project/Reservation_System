from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal
from models import Room

app = Flask(__name__)


@app.route('/available_rooms')
def get_rooms():
    try:
        with SessionLocal() as session:
            rooms = session.query(Room).all()
            available_rooms = [room.room_number for room in rooms if not room.is_reserved]
            return jsonify(available_rooms)

    except SQLAlchemyError as e:
        print(f'Database Error: {e}')


if __name__ == '__main__':
    app.run(debug=True)
