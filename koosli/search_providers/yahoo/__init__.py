import json
import random
import os

from flask import current_app
from requests_oauthlib import OAuth1
import requests


class _YahooBase(object):

    def kapify_response(self, yahoo_response):
        response = []
        for result in yahoo_response.get('bossresponse', {}).get('web', {}).get('results', []):
            response.append({
                'title': result['title'],
                'displayUrl': result['dispurl'],
                'description': result['abstract'],
                'url': result['url'],
            })
        return response


class YahooMock(_YahooBase):

    def search(self, query):
        with open(os.path.join(os.path.dirname(__file__), 'mock-responses', 'search.json')) as f:
            results = json.load(f)
        random.shuffle(results['bossresponse']['web']['results'])
        return self.kapify_response(results)


class Yahoo(_YahooBase):

    api_root = 'https://yboss.yahooapis.com/ysearch/web'

    def search(self, query):
        client_key = current_app.config['YAHOO_CONSUMER_KEY']
        client_secret = current_app.config['YAHOO_CONSUMER_SECRET']
        oauth = OAuth1(
            client_key=client_key,
            client_secret=client_secret,
        )
        params = {
            'format': 'json',
            'q': "'%s'" % query,
            'count': 10,
        }
        response = requests.get(self.api_root, params=params, auth=oauth)
        response.raise_for_status()
        return self.kapify_response(response.json())
