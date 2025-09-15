from sqlalchemy.orm import relationship
from config.database import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    subsidiary_id = db.Column(db.Integer, ForeignKey('subsidiaries.id'), nullable=False)
    # ip_address = db.Column(db.Integer, ForeignKey("ip_addresses.id"), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    patronymic = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    office_id = db.Column(db.Integer, ForeignKey('offices.id'), nullable=False)
    password = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    personal_phone = db.Column(db.String(20), nullable=True)
    position = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.TIMESTAMP, server_default=func.now())

    # Many-to-Many connection with Access
    accesses = db.relationship('Access', secondary='user_accesses', back_populates='users')
    docs = relationship("Documents", back_populates="author")
    news = relationship("News", back_populates="author")

class UserAccess(db.Model):
    __tablename__ = 'user_accesses'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    access_id = db.Column(db.Integer, db.ForeignKey('accesses.id'), primary_key=True)

class Subsidiary(db.Model):
    __tablename__ = 'subsidiaries'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    slug = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(40), nullable=True)

class Office(db.Model):
    __tablename__ = 'offices'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    subsidiary_id = db.Column(db.Integer, ForeignKey('subsidiaries.id'), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(40), nullable=True)


