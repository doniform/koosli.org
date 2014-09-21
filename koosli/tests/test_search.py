from koosli.tests import TestCase

class SearchTest(TestCase):

    def test_main_page(self):
        self._test_get_request('/', 'index.html')

    def test_about(self):
        self._test_get_request('/about', 'about.html')

    def test_beneficiaries(self):
        self._test_get_request('/beneficiaries', 'beneficiaries.html')

    def test_search_providers(self):
        self._test_get_request('/search_providers', 'search_providers.html')

    def test_advertisers(self):
        self._test_get_request('/advertisers', 'advertisers.html')

    def test_search(self):
        self._test_get_request('/search?q=foobar', 'search_results.html')
