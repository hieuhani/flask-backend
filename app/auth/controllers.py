from app.helpers import validate_json
from flask import request, jsonify
from marshmallow import ValidationError
from app.users.models import User, Contact
from sqlalchemy.exc import SQLAlchemyError
from app import db
from . import auth
from .schemas import sign_up_request_schema, sign_in_request_schema
from app.users.schemas import UserSchema


def response_auth(user):
    token = user.generate_auth_token(7 * 24 * 60 * 60)  # Token will be expired in 7 days
    return jsonify({
        'user': UserSchema(exclude=['contacts']).dump(user),
        'token': token,
    })


@auth.route('/sign_in', methods=['POST'])
@validate_json
def sign_in():
    payload = request.get_json()
    try:
        auth_payload = sign_in_request_schema.load(payload)
    except ValidationError as err:
        return jsonify(err.messages), 422

    contact = Contact.query.filter_by(value=auth_payload['contact']).first()
    if not contact:
        return jsonify('The account does not exists'), 400

    return response_auth(contact.user)


@auth.route('/sign_up', methods=['POST'])
@validate_json
def sign_up():
    payload = request.get_json()
    try:
        auth_payload = sign_up_request_schema.load(payload)
    except ValidationError as err:
        return jsonify(err.messages), 422

    current_contact = Contact.query.filter_by(value=auth_payload['email']).first()
    if current_contact:
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

    return response_auth(user)
