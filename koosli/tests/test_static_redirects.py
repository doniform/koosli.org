from . import NonContextualTestCase

class SearchFailureTest(NonContextualTestCase):

    def test_redirects(self):
        for url in ('/robots.txt',):
            response = self.client.get(url)
            self.assert302(response)
