from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    contacts = fields.Nested('ContactSchema', many=True)


class ContactSchema(Schema):
    id = fields.String(required=True)
    type = fields.Integer(required=True)
    value = fields.String(required=True)
    verified = fields.Boolean(required=True)


user_schema = UserSchema()
contact_schema = ContactSchema()
