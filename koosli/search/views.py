from flask import Blueprint, render_template, request, flash, abort, current_app
from requests import HTTPError
from geoip import geolite2
from logging import getLogger
import importlib

from koosli import db, log_generic_error
from koosli.user.models import User, UserStats
from .models import UserQuery


mod = Blueprint('search', __name__, url_prefix='/search')
_logger = getLogger(__name__)


def get_search_providers():
    """ Get a list of the search providers, in preferred order. """
    providers = []
    for provider in ('yahoo', 'bing'):
        providers.append(current_app.config['SEARCH_PROVIDERS'][provider]())
    return providers


def perform_query_or_die_trying(query):
    """ Run a query against all backend search providers until one succeeds, or blow up. """
    providers = get_search_providers()
    for index, provider in enumerate(providers):
        try:
            return provider.search(query)
        except HTTPError as error:
            log_generic_error(error)
            if index + 1 < len(providers):
                flash('%s backend failed, falling back to %s.' % (
                    provider.human_readable, providers[index+1].human_readable), 'warning')
            else:
                flash('Yikes, %s failed too!' % provider.human_readable, 'warning')
    else:
        flash("All search providers failed to respond properly. I'm deeply ashamed.",
            'danger')
        abort(503)


def get_country_code_from_ip(ip):
    """ Get the country code from the given IP, or return an empty string if nothing was found. """
    try:
        match = geolite2.lookup(ip)
        if match:
            return match.country
    except AttributeError:
        # Windows, not supported by geoip, just ignore as it doesn't matter in prod
        _logger.warning('GeoIP lookup failed')
    return ''


@mod.route('')
def do_search():
    query = request.args.get('q', '').strip()
    if query:
        api_response = perform_query_or_die_trying(query)
    else:
        api_response = {
            'results': [],
        }
    context = {
        'results': api_response['results'],
        'query': query,
        'ads_token': api_response.get('ads_token'),
    }

    country = ''
    if request.access_route:
        originating_ip = request.access_route[0]
        country = get_country_code_from_ip(originating_ip)
    query_record = UserQuery(
        query_string=query,
        location=country)
    db.session.add(query_record)
    db.session.commit()

    return render_template('search_results.html', **context)
