from sqlalchemy.orm import relationship
from config.database import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func


class Documents(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    path = db.Column(db.String(255))
    description = db.Column(db.String(255))
    creation_date = db.Column(db.TIMESTAMP, server_default=func.now())

    author = relationship('User', back_populates='docs')
