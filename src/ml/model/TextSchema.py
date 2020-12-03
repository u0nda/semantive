from marshmallow import fields
from src.ml.model import MLSchema


class TextSchema(MLSchema):
    """
    Text Schema
    """
    id = fields.Int(dump_only=True)
    text_content = fields.Str(required=False)
