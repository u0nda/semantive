from marshmallow import fields, Schema


class MLSchema(Schema):
    """
    ML Schema
    """
    name = fields.Str(required=True)
    url = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
