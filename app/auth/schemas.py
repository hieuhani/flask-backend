from marshmallow import Schema, fields


class SignUpRequestSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


class SignInRequestSchema(Schema):
    contact = fields.String(required=True)
    password = fields.String(required=True)


sign_up_request_schema = SignUpRequestSchema()
sign_in_request_schema = SignInRequestSchema()
