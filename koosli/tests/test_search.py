from flask import url_for
from mock import patch
from requests import HTTPError

import unittest
import os
from koosli import create_app
from koosli.tests import TestCase
from koosli.views.search import get_search_providers

class FailureProvider(object):
    """ Search provider that fails. """
    human_readable = 'FailureProvider'

    def search(self, query):
        raise HTTPError()


class SearchTest(TestCase):

    def test_main_page(self):
        self._test_get_request(url_for('search.search_main'), 'index.html')

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


class SearchFailureTest(unittest.TestCase):

    def setUp(self):
        test_config = os.path.join(os.path.dirname(__file__), 'test_config.py')
        self.app = create_app(test_config)
        self.client = self.app.test_client()
        for helper in (200, 201, 400, 401, 403, 404, 500, 503):
            setattr(self, 'assert%d' % helper, self._assert_status_code(helper))


    def _assert_status_code(self, code):
        """ Helper to create `self.assertXXX` helpers. """
        def _wrapped(response):
            self.assertEqual(response.status_code, code)
        return _wrapped


    def test_single_search_provider_failure(self):
        with self.app.app_context():
            real_providers = get_search_providers()
        first_provider_failing = [FailureProvider()] + real_providers
        #from nose.tools import set_trace as f; f()
        self.app.testing = True
        with patch('koosli.views.search.get_search_providers', lambda: first_provider_failing):
            response = self.client.get('/search?q=kittens')
            self.assert200(response)
            self.assertTrue('FailureProvider backend failed' in response.data)


    def test_all_rpviders_failing(self):
        only_failing_providers = [FailureProvider()]
        with patch('koosli.views.search.get_search_providers', lambda: only_failing_providers):
            response = self.client.get('/search?q=kittens')
            self.assert503(response)
            self.assertTrue('All search providers failed' in response.data)
