from app.helpers import validate_json
from flask import request, jsonify
from marshmallow import ValidationError
from app.users.models import User, Contact
from sqlalchemy.exc import SQLAlchemyError
from app import db
from . import auth
from .schemas import sign_up_request_schema
from app.users.schemas import UserSchema


@auth.route('/login', methods=['POST'])
def login():
    return 'hello world'


@auth.route('/sign_up', methods=['POST'])
@validate_json
def sign_up():
    payload = request.get_json()
    try:
        auth_payload = sign_up_request_schema.load(payload)
    except ValidationError as err:
        return jsonify(err.messages), 422

    current_contact = Contact.query.filter_by(value=auth_payload['email']).first()
    if current_contact and current_contact.verified:
        return jsonify('This contact has been registered'), 400

    try:
        user = User(first_name=auth_payload['first_name'],
                    last_name=auth_payload['last_name'],
                    password=auth_payload['password'])
        db.session.add(user)
        db.session.commit()

        contact = Contact(user_id=user.id,
                          type=1,
                          value=auth_payload['email'])
        db.session.add(contact)

        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify(err), 500

    token = user.generate_auth_token(7 * 24 * 60 * 60)  # Token will be expired in 7 days

    return jsonify({
        'user': UserSchema(exclude=['contacts']).dump(user),
        'token': token,
    })
