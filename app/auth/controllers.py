from graphql import GraphQLError
from app.users.models import User, Contact
from sqlalchemy.exc import SQLAlchemyError
from app import db


def response_auth(user):
    token = user.generate_auth_token(7 * 24 * 60 * 60)  # Token will be expired in 7 days
    return token, user


def sign_in(payload):
    contact = Contact.query.filter_by(value=payload['contact']).first()
    if not contact:
        raise GraphQLError('The account does not exists')
    if not contact.user.verify_password(payload['password']):
        raise GraphQLError('Wrong password')

    return response_auth(contact.user)


def sign_up(payload):
    current_contact = Contact.query.filter_by(value=payload['email']).first()
    if current_contact:
        raise GraphQLError('This contact has been registered')

    try:
        user = User(first_name=payload['first_name'],
                    last_name=payload['last_name'],
                    password=payload['password'])
        db.session.add(user)
        db.session.commit()

        contact = Contact(user_id=user.id,
                          type=1,
                          value=payload['email'])
        db.session.add(contact)

        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        raise GraphQLError(err)

    return response_auth(user)
