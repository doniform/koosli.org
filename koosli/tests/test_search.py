from koosli.tests import TestCase

class SearchTest(TestCase):

    def test_main_page(self):
        self._test_get_request('/', 'index.html')

    def test_search(self):
        self._test_get_request('/search?q=foobar', 'search_results.html')
