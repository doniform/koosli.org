import unittest

from koosli import create_app

class SearchTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


    def test_search(self):
        response = self.client.get('/search?q=foobar')
        self.assertEqual(response.status_code, 200)
