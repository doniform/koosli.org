from flask import Blueprint, current_app, render_template, request
from koosli.user.forms import RegistrationForm
import importlib

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


def get_search_provider():
    klass = current_app.config['SEARCH_PROVIDERS']['yahoo']
    return klass()


@mod.route('/search')
def do_search():
    provider = get_search_provider()
    query = request.args.get('q', '').strip()
    if query:
        api_response = provider.search(query)
    else:
        api_response = {
            'results': [],
            'ads_token': '',
        }
    context = {
        'results': api_response['results'],
        'query': query,
        'ads_token': api_response['ads_token'],
    }
    return render_template('search_results.html', **context)
