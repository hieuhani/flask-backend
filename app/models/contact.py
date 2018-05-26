from sqlalchemy.dialects.postgresql import UUID
from app import db


class Contact(db.Model):
    __tablename__ = 'contacts'

    # Properties
    id = db.Column(UUID, primary_key=True)
    user_id = db.Column(UUID, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)

    # Relations
    # user = db.relationship('user', back_populates='contacts')
