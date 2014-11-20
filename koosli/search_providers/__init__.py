
from flask import current_app

def get_search_provider():
    klass = current_app.config['SEARCH_PROVIDERS']['yahoo']
    return klass()
