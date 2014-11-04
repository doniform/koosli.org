import json
import random
import os

from flask import current_app, Markup
from requests_oauthlib import OAuth1
from urllib import quote_plus
import requests


class _YahooBase(object):

    human_readable = 'Yahoo!'

    def kapify_response(self, yahoo_response):
        ads_token = yahoo_response['bossresponse'].get('ads', {}).get('dmtoken')
        response = {
            'ads_token': Markup(ads_token),
            'results': [],
        }
        for result in yahoo_response.get('bossresponse', {}).get('web', {}).get('results', []):
            # Wrapping the data in Markup() ensures they're not escaped in the template rendering.
            # We trust results from Yahoo.
            response['results'].append({
                'title': Markup(result['title']),
                'displayUrl': Markup(result['dispurl']),
                'description': Markup(result['abstract']),
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

    api_root = 'https://yboss.yahooapis.com/ysearch/web,ads'

    def search(self, query):
        client_key = current_app.config['YAHOO_CONSUMER_KEY']
        client_secret = current_app.config['YAHOO_CONSUMER_SECRET']
        oauth = OAuth1(
            client_key=client_key,
            client_secret=client_secret,
        )
        params = {
            'format': 'json',
            # For some reason BOSS auth fails for multi-word searches if we don't escape the values
            # ourselves due to invalid signatures. If you want to dig to figure out why, go ahead.
            'q': quote_plus(query),
            'count': 10,
            'ads.Partner': 'domaindev_syn_boss157_ss_search',
            'ads.Type': 'ddc_koosli_org',
        }
        response = requests.get(self.api_root, params=params, auth=oauth)
        response.raise_for_status()
        return self.kapify_response(response.json())
