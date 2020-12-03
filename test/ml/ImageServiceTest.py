import json
import unittest
from src.app import create_app, db


class ImageServiceTest(unittest.TestCase):
    """
    Image Service Test Case
    """

    def setUp(self):
        """
        Test Setup
        """
        self.app = create_app("test")
        self.client = self.app.test_client
        self.endpoint = '/semantive/img/'
        self.content_type = 'application/json'
        self.body = {
            'name': 'semantive_blog_page',
            'url': 'https://semantive.com'
        }
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_save_image_to_db_succesful(self):
        """ Test saving image to db """
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(self.body))
        self.assertEqual(201, res.status_code)

    def test_save_image_to_db_wrong_req_body(self):
        """ Test saving image to db """
        body = {
            'url': 'https://semantive.com/image-summarization-in-python/'
        }
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(body))
        self.assertEqual(400, res.status_code)

    def test_save_image_and_check_status(self):
        """ Test saving image to db """
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(self.body))
        self.assertEqual(201, res.status_code)

        res = self.client().get(
        self.endpoint + "status",
        headers={'Content-Type': self.content_type})
        json_data = json.loads(res.data)
        self.assertEqual("recent task completed", json_data)


    def test_get_image(self):
        """ Test get image """
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(self.body))
        self.assertEqual(201, res.status_code)
        json_data = json.loads(res.data)['Images stored with IDs'][0]

        res = self.client().get(
            self.endpoint + str(json_data),
            headers={'Content-Type': "image/*"})
        self.assertEqual(200, res.status_code)

    def test_delete_image(self):
        """ Test delete image"""
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(self.body))
        self.assertEqual(201, res.status_code)
        json_data = json.loads(res.data)['Images stored with IDs'][0]

        res = self.client().delete(
            self.endpoint + str(json_data),
            headers={'Content-Type': self.content_type})
        self.assertEqual(200, res.status_code)

    def test_delete_image_with_id_not_found(self):
        """ Test delete image"""
        res = self.client().delete(
            self.endpoint + '0',
            headers={'Content-Type': self.content_type})
        json_data = json.loads(res.data)
        self.assertEqual(404, res.status_code)
        self.assertTrue(json_data.get("error"), "content not found for id: 0")


    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
