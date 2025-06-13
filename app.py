from flask import Flask
from routes.rooms import rooms_bp
from routes.reservations import reservation_bp

app = Flask(__name__)

app.register_blueprint(rooms_bp)
app.register_blueprint(reservation_bp)


if __name__ == '__main__':
    app.run(debug=True)
