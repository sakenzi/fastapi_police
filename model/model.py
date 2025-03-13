from sqlalchemy import Boolean, String, Integer, DateTime, Float, ForeignKey, Date, func, Column, BigInteger, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base
from typing import Optional
from geoalchemy2 import Geometry
import enum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), default="", nullable=True)
    last_name = Column(String(50), default="", nullable=True)
    uin = Column(String(12), nullable=True)
    email = Column(String(50), default="", nullable=True)
    phone_number = Column(String(30), nullable=True)
    password = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=False)
    verification_code = Column(String(6), nullable=True)
    birth_day = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    photo = Column(String(255), nullable=True)

    created_at: Optional[datetime] = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    
    geolocation_id = Column(Integer, ForeignKey('geolocations.id', ondelete='CASCADE'), nullable=True)

    geolocation = relationship("Geolocation", back_populates="user")
    statements = relationship("Statement", foreign_keys="Statement.user_id", back_populates="user")
    session_calls = relationship("SessionCall", foreign_keys="SessionCall.user_id", back_populates="user")

class Policeman(Base):
    __tablename__ = "policemans"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), default="", nullable=True)
    last_name = Column(String(50), default="", nullable=True)
    email = Column(String(50), unique=True, nullable=True)
    phone_number = Column(String(20), nullable=True)
    photo = Column(String(255), nullable=True)
    rank = Column(String(255), default="", nullable=True)
    birth_day = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False)
    verification_code = Column(String(6), nullable=True)
    
    created_at: Optional[datetime] = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    station_id = Column(Integer, ForeignKey('stations.id', ondelete='CASCADE'), nullable=True)

    station = relationship("Station", back_populates="policeman")
    session_calls = relationship("SessionCall", foreign_keys="SessionCall.policeman_id", back_populates="policeman")

class Geolocation(Base):
    __tablename__ = "geolocations"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(255), default="", nullable=True)
    street = Column(String(255), default="", nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    user = relationship("User", back_populates="geolocation")
    station = relationship("Station", back_populates="geolocation")

class Statement(Base):
    __tablename__ = "statements"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, default="", nullable=True)

    created_at: Optional[datetime] = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    type_id = Column(Integer, ForeignKey('types.id', ondelete='CASCADE'), nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="statements")
    type = relationship("Type", foreign_keys=[type_id], back_populates="statements")

class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(100), nullable=True)

    statements = relationship("Statement", foreign_keys="Statement.type_id", back_populates="type")

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String(100), nullable=True)

    geolocation_id = Column(Integer, ForeignKey('geolocations.id', ondelete='CASCADE'), nullable=True)

    policeman = relationship("Policeman", back_populates="station")
    geolocation = relationship("Geolocation", back_populates="station")

class SessionCall(Base):
    __tablename__ = "session_calls"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, nullable=True)

    created_at: Optional[datetime] = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    policeman_id = Column(Integer, ForeignKey('policemans.id', ondelete='CASCADE'), nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="session_calls")
    policeman = relationship("Policeman", foreign_keys=[policeman_id], back_populates="session_calls")

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=True)
    password = Column(String(255), nullable=True)


class Crime(Base):
    __tablename__ = "crimes"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String(255), default="", nullable=True)
    street = Column(String(255), default="", nullable=True)
    geoposition = Column(String(255), default="", nullable=True)
    period = Column(String(255), default="", nullable=True)
    stat = Column(String(255), default="", nullable=True)
    time_period = Column(String(255), default="", nullable=True)
    organ = Column(String(255), default="", nullable=True)
    year = Column(String(255), default="", nullable=True)
    crime_code = Column(String(255), default="", nullable=True)
    hard_code = Column(String(255), default="", nullable=True)
    city_code = Column(String(255), default="", nullable=True)
    ud = Column(String(255), default="", nullable=True)
    objectid = Column(String(255), default="", nullable=True)
    home_number = Column(String(255), default="", nullable=True)
    reg_code = Column(String(255), default="", nullable=True)
    geom = Column(Geometry("POINT", srid=4326))