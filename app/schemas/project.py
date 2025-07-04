from marshmallow import Schema, fields, validate

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str()
    link = fields.Url(required=False)
    screenshot = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
