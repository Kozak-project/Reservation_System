from .reservations import reservations_bp
from .users import users_bp
from .rooms import rooms_bp


def register_routes(app):
    app.register_blueprint(reservations_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(rooms_bp)
