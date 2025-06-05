from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    phone_number = Column(String(45), nullable=False)

    reservations = relationship('Reservation', back_populates='user')


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(Integer, nullable=False)
    price_per_night = Column(Numeric(precision=10, scale=2), nullable=False)
    is_reserved = Column(Boolean, nullable=False)
    reserved_by = Column(String(45), nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    reservations = relationship('Reservation', back_populates='room')


class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,ForeignKey('user.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    room = relationship('Room', back_populates='reservations')
    user = relationship('User', back_populates='reservations')
