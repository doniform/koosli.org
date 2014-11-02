import base64
import json
import os
import random

from flask import current_app
import requests

class _BingBase(object):

    def kapify_response(self, bing_response):
        response = []
        for result in bing_response.get('d', {}).get('results', []):
            response.append({
                'displayUrl': result['DisplayUrl'],
                'description': result['Description'],
                'url': result['Url'],
                'title': result['Title'],
            })
        return response


class BingMock(_BingBase):

    def search(self, query):
        with open(os.path.join(os.path.dirname(__file__), 'mock-responses', 'search.json')) as f:
            results = json.load(f)
            random.shuffle(results['d']['results'])
            return self.kapify_response(results)


class Bing(_BingBase):
    api_root = 'https://api.datamarket.azure.com/Bing/Search/Web'

    def search(self, query):
        params = {
            '$format': 'json',
            'Query': "'%s'" % query,
        }
        account_key = current_app.config.get('BING_API_KEY')
        headers = {
            'Authorization': 'Basic %s' % (base64.b64encode('{0}:{0}'.format(account_key))),
        }
        response = requests.get(self.api_root, params=params, headers=headers)
        return self.kapify_response(response.json())
