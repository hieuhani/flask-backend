from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

from . import db

class User(db.Model):
    __tablename__ = 'users'

    # Properties
    id = db.Column(UUID, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    # Relations
    contacts = db.relationship('Contact', backref='user')

class Contact(db.Model):
    __tablename__ = 'contacts'

    # Properties
    id = db.Column(UUID, primary_key=True)
    user_id = db.Column(UUID, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)

    # Relations
    user = db.relationship('User', back_populates='contacts')
