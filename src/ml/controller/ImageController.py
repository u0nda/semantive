import base64
import re
import uuid

from flask import request, Blueprint, json, Response
import requests
from ..utils.AppLogger import logging
from ..utils.StatusCheck import status_pending, status_completed, c
from ..exceptions.Exceptions import notFoundError, valid
from ..model.ImageModel import ImageModel
from ..model.ImageSchema import ImageSchema
from bs4 import BeautifulSoup

img_api = Blueprint('img_api', __name__)
img_schema = ImageSchema()

@img_api.route('/', methods=['POST'])
def save():
    """
    Save Image from web to db
    """
    if not valid(request.get_json()):
        return custom_response("request body not valid", 400)

    status_pending()
    logging.info('status set as pending')

    name = request.get_json()['name']
    url = request.get_json()['url']

    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')

    img_tags = soup.find_all('img')
    links = [img['src'] for img in img_tags]

    ids = []
    for link in links:
        if 'base64' not in link:
            if 'http' not in link:
                #add base url if img src is relative
                link = '{}{}'.format(url, link)
            response = requests.get(link)
            logging.info(link)


        image = base64.b64encode(response.content)
        id = uuid.uuid1().time

        data = {
            "id": id,
            "name": name,
            "url": url,
            "image_content": image
        }

        insert = ImageModel(data)
        insert.save()

        logging.info('status set as completed, Image saved to db')

        ids.append(str(id))

    status_completed()
    ids_data = {
        "Images stored with IDs": ids
    }
    return custom_response(ids_data, 201)


@img_api.route('/status', methods=['GET'])
def get_status():
    """
    Get status for recent Image task
    """
    if c.get('status') is None:
        status = 'task not started'
    else:
        status = c.get('status')
    return custom_response(status, 200)


@img_api.route('/', methods=['GET'])
def get_all():
    """
    Get All saved Images
    """
    all_args = request.args
    insert = ImageModel.get_all_images(all_args)
    data = img_schema.dump(insert, many=True)

    logging.info('get all tasks')
    return custom_response(data, 200)


@img_api.route('/<int:img_id>', methods=['GET'])
def get_one(img_id):
    """
    Get partucular Image
    """
    insert = ImageModel.get_one_image(img_id)

    if notFoundError(img_id, insert):
        return custom_response({'error': 'content not found for id: ' + str(img_id)}, 404)

    data = img_schema.dump(insert)
    image = base64.b64decode(data['image_content'])
    logging.info('get particular task')

    return custom_response_4get(image, 200)


@img_api.route('/<int:img_id>', methods=['DELETE'])
def delete(img_id):
    """
    Delete A Image
    """
    insert = ImageModel.get_one_image(img_id)
    if notFoundError(img_id, insert):
        return custom_response({'error': 'content not found for id: ' + str(img_id)}, 404)

    insert.delete()
    logging.info('task deleted')
    return custom_response({'message': 'deleted'}, 200)


def custom_response_4get(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="image/*",
        response=res,
        status=status_code
    )


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
