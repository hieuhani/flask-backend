from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app
from app import db


class User(db.Model):
    __tablename__ = 'users'

    # Properties
    id = db.Column(UUID, primary_key=True, server_default=db.text('gen_random_uuid()'))
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String)

    # Relations
    contacts = db.relationship('Contact', backref='user')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in):
        serializer = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)

        return serializer.dumps({
            'id': self.id,
        }).decode('ascii')


class Contact(db.Model):
    __tablename__ = 'contacts'

    # Properties
    id = db.Column(UUID, primary_key=True, server_default=db.text('gen_random_uuid()'))
    user_id = db.Column(UUID, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.SmallInteger, nullable=False)
    value = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
