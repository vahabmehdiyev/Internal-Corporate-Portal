from config.database import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from api.users.users_model import User

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    is_pinned = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=func.now())

    author = relationship('User', back_populates='news')