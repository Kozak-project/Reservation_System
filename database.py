from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    phone_number = Column(String(45), nullable=False)


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(Integer, nullable=False)
    price_per_night = Column(Numeric(precision=10, scale=2), nullable=False)
    is_reserved = Column(Boolean, nullable=False)
    reserved_by = Column(String(45), nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)


class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    room_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
