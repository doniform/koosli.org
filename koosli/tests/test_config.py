import os

from koosli.search_providers import bing


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

DEBUG = True

SECRET_KEY = 'not a secret'


#=========================================
# Search Providers
#=========================================

#BING_API_KEY = '' # Fill in to use live bing search

SEARCH_PROVIDERS = {
    'bing': bing.BingMock,
    #'bing': bing.Bing,
}

#=========================================
# Database Config
#=========================================

# Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
SQLALCHEMY_ECHO = True

# SQLITE for prototyping.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT + '/koosli_test.sqlite'
