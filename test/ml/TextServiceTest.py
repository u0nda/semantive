import json
import unittest
from src.app import create_app, db


class TextServiceTest(unittest.TestCase):
    """
    Text Service Test Case
    """

    def setUp(self):
        """
        Test Setup
        """
        self.app = create_app("test")
        self.client = self.app.test_client
        self.endpoint = '/semantive/txt/'
        self.content_type = 'application/json'
        self.body = {
            'name': 'semantive_blog_page',
            'url': 'https://semantive.com/text-summarization-in-python/'
        }
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_save_text_to_db_succesful(self):
        """ Test saving text to db """
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(self.body))
        self.assertEqual(201, res.status_code)

    def test_save_text_to_db_wrong_req_body(self):
        """ Test saving text to db """
        body = {
            'url': 'https://semantive.com/text-summarization-in-python/'
        }
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(body))
        self.assertEqual(400, res.status_code)

    def test_save_text_and_check_status(self):
        """ Test saving text to db """
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


    def test_get_text(self):
        """ Test get text """
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(self.body))
        self.assertEqual(201, res.status_code)
        json_data = json.loads(res.data)

        res = self.client().get(
            self.endpoint + str(json_data.get('id')),
            headers={'Content-Type': self.content_type})
        json_data = json.loads(res.data)
        self.assertEqual(200, res.status_code)
        self.assertEqual('semantive_blog_page', json_data.get('name'))

    def test_update_text(self):
        """ Test update text """
        body = {
            'name': 'brand new name',
            'url': 'https://semantive.com/text-summarization-in-python/'
        }
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(self.body))
        self.assertEqual(201, res.status_code)
        json_data = json.loads(res.data)

        res = self.client().put(
            self.endpoint + str(json_data.get('id')),
            headers={'Content-Type': self.content_type},
            data=json.dumps(body))
        json_data = json.loads(res.data)
        print(res.status_code)
        self.assertEqual(200, res.status_code)
        self.assertEqual(json_data.get('name'), 'brand new name')

    def test_update_text_wrong_req_body(self):
        """ Test update text """
        body = {
            'name': 'brand new name'
        }
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(self.body))
        self.assertEqual(201, res.status_code)
        json_data = json.loads(res.data)

        res = self.client().put(
            self.endpoint + str(json_data.get('id')),
            headers={'Content-Type': self.content_type},
            data=json.dumps(body))
        print(res.status_code)
        self.assertEqual(400, res.status_code)

    def test_delete_text(self):
        """ Test delete text"""
        res = self.client().post(
            self.endpoint,
            headers={'Content-Type': self.content_type},
            data=json.dumps(self.body))
        self.assertEqual(201, res.status_code)
        json_data = json.loads(res.data)

        res = self.client().delete(
            self.endpoint + str(json_data.get('id')),
            headers={'Content-Type': self.content_type})
        self.assertEqual(200, res.status_code)

    def test_delete_text_with_id_not_found(self):
        """ Test delete text"""
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
