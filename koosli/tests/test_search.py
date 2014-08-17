import os
import unittest

from koosli import create_app

class SearchTest(unittest.TestCase):

    def setUp(self):
        test_config = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_config.py'))
        self.app = create_app(config_file=test_config)
        self.client = self.app.test_client()


    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


    def test_search(self):
        response = self.client.get('/search?q=foobar')
        self.assertEqual(response.status_code, 200)
