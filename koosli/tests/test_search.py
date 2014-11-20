from . import TestCase, NonContextualTestCase
from .. import create_app

from koosli.search.views import get_search_providers
from koosli.search.models import UserQuery

from flask import url_for
from mock import patch
from requests import HTTPError
import os


class FailureProvider(object):
    """ Search provider that fails. """
    human_readable = 'FailureProvider'

    def search(self, query):
        raise HTTPError()


class SearchTest(TestCase):

    def test_main_page(self):
        self._test_get_request('/beta', 'index.html')

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

    def test_empty_search(self):
        self._test_get_request('/search?q=', 'search_results.html')

    def test_querymodel_added(self):
        self.assertEqual(UserQuery.query.count(), 0)
        response = self.client.get('/search?q=foobar')
        self.assertEqual(UserQuery.query.count(), 1)


class SearchFailureTest(NonContextualTestCase):

    def test_single_search_provider_failure(self):
        with self.app.app_context():
            real_providers = get_search_providers()
        first_provider_failing = [FailureProvider()] + real_providers
        self.app.testing = True
        with patch('koosli.search.views.get_search_providers', lambda: first_provider_failing):
            response = self.client.get('/search?q=kittens')
            self.assert200(response)
            self.assertTrue('FailureProvider backend failed' in response.data)


    def test_all_providers_failing(self):
        only_failing_providers = [FailureProvider()]
        with patch('koosli.search.views.get_search_providers', lambda: only_failing_providers):
            response = self.client.get('/search?q=kittens')
            self.assert503(response)
            self.assertTrue('All search providers failed' in response.data)
