from marshmallow import fields
from src.ml.model import MLSchema


class ImageSchema(MLSchema):
    """
    Image Schema
    """
    id = fields.Integer(required=True)
    image_content = fields.Str(required=False)
