import os

from koosli.search_providers import bing


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

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
SQLALCHEMY_ECHO = False

# Postgres for production.
SQLALCHEMY_DATABASE_URI = 'psql://username:password@server/db?charset=utf8'
