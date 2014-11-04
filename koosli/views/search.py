from koosli import log_generic_error
from koosli.user.forms import RegistrationForm

from flask import Blueprint, current_app, render_template, request, flash, abort
from requests import HTTPError

mod = Blueprint('search', __name__)

@mod.route('/beta')
def search_main():
    return render_template('index.html')

@mod.route('/')
def splash():
    form = RegistrationForm(request.form)
    return render_template('splash.html', form=form)


@mod.route('/about')
def about():
    return render_template('about.html')

@mod.route('/beneficiaries')
def beneficiaries():
    return render_template('beneficiaries.html')

@mod.route('/search_providers')
def search_providers():
    return render_template('search_providers.html')

@mod.route('/advertisers')
def advertisers():
    return render_template('advertisers.html')


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



@mod.route('/search')
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
    return render_template('search_results.html', **context)
