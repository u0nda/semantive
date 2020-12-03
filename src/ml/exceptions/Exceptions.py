from marshmallow import ValidationError
from src.ml.model.TextSchema import TextSchema
from src.ml.utils.AppLogger import logging

text_schema = TextSchema()


def valid(request_data):
    try:
        data = text_schema.load(request_data)
        return True
    except ValidationError:
        logging.info('Validation Error')
        return False


def notFoundError(txt_id, insert):
    if not insert:
        logging.info('Not Found Error')
        return True
