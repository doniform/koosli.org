from flask import Blueprint, current_app, render_template, request
import importlib

mod = Blueprint('search', __name__)

@mod.route('/')
def search_main():
    return render_template('index.html')


def get_search_provider():
    klass = current_app.config['SEARCH_PROVIDERS']['bing']
    return klass()


@mod.route('/search')
def do_search():
    provider = get_search_provider()
    query = request.args.get('q')
    results = provider.search(query).get('d', {}).get('results', [])
    return render_template('search_results.html', results=results, query=query)
