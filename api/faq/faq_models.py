from sqlalchemy.orm import relationship
from config.database import db
from sqlalchemy import ForeignKey


class FAQ(db.Model):
    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, ForeignKey('sections.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    section = relationship("Section", back_populates="faqs")

class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    faqs = relationship('FAQ', back_populates='section')