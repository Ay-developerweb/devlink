from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserProfileSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    role = fields.Str()
    created_at = fields.DateTime()
