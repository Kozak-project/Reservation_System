from flask import Flask
from routes.rooms import rooms_bp
from routes.reservations import reservations_bp
from routes.users import users_bp

app = Flask(__name__)

app.register_blueprint(rooms_bp)
app.register_blueprint(reservations_bp)
app.register_blueprint(users_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
