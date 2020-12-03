from flask import request, Blueprint, json, Response
import requests
from ..utils.AppLogger import logging
from ..utils.StatusCheck import status_pending, status_completed, c
from ..exceptions.Exceptions import notFoundError, valid
from ..model.TextModel import TextModel
from ..model.TextSchema import TextSchema
from bs4 import BeautifulSoup

txt_api = Blueprint('txt_api', __name__)
text_schema = TextSchema()

@txt_api.route('/', methods=['POST'])
def save():
    """
    Save Text from web to db
    """
    if not valid(request.get_json()):
        return custom_response("request body not valid", 400)

    status_pending()
    logging.info('status set as pending')

    name = request.get_json()['name']
    url = request.get_json()['url']

    text = requests.get(url).text
    soup = BeautifulSoup(text, 'html.parser')
    all_text = ''
    for p in soup.find_all('p'):
        text2 = p.get_text().replace('\n', '')
        all_text += text2

    data = {
        "name": name,
        "url": url,
        "text_content": all_text
    }

    insert = TextModel(data)
    insert.save()

    # return serialized data in response:
    data = text_schema.dump(insert)

    status_completed()
    logging.info('status set as completed, text saved to db')

    return custom_response(data, 201)


@txt_api.route('/status', methods=['GET'])
def get_status():
    """
    Get status for recent Text task
    """
    if c.get('status') is None:
        status = 'task not started'
    else:
        status = c.get('status')
    return custom_response(status, 200)

@txt_api.route('/', methods=['GET'])
def get_all():
    """
    Get All saved Texts
    """
    all_args = request.args
    insert = TextModel.get_all_text(all_args)
    data = text_schema.dump(insert, many=True)
    logging.info('get all tasks')
    return custom_response(data, 200)

@txt_api.route('/<int:txt_id>', methods=['GET'])
def get_one(txt_id):
    """
    Get partucular Text
    """
    insert = TextModel.get_one_text(txt_id)

    if notFoundError(txt_id, insert):
        return custom_response({'error': 'content not found for id: ' + str(txt_id)}, 404)

    data = text_schema.dump(insert)
    logging.info('get particular task')
    return custom_response(data, 200)

@txt_api.route('/<int:txt_id>', methods=['PUT'])
def update(txt_id):
    """
    Update A Text
    """

    insert = TextModel.get_one_text(txt_id)
    if notFoundError(txt_id, insert):
        return custom_response({'error': 'content not found for id: ' + str(txt_id)}, 404)

    if not valid(request.get_json()):
        return custom_response("request body not valid", 400)

    data = text_schema.load(request.get_json())
    insert.update(data)

    data = text_schema.dump(insert)
    logging.info('task updated')
    return custom_response(data, 200)

@txt_api.route('/<int:txt_id>', methods=['DELETE'])
def delete(txt_id):
    """
    Delete A Text
    """
    insert = TextModel.get_one_text(txt_id)
    if notFoundError(txt_id, insert):
        return custom_response({'error': 'content not found for id: ' + str(txt_id)}, 404)

    insert.delete()
    logging.info('task deleted')
    return custom_response({'message': 'deleted'}, 200)

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
