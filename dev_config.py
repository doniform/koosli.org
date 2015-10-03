import os

from koosli.search_providers import bing, yahoo

DEBUG = True

SECRET_KEY = 'not a secret'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

SPLASH_REGISTRATION = True

#=========================================
# Database Config
#=========================================

# Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
SQLALCHEMY_ECHO = True

SEARCH_PROVIDERS = {
    'yahoo': yahoo.YahooMock,
    'bing': bing.BingMock,
}

# SQLITE for prototyping.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT + '/kooslidb.db'

YAHOO_CONSUMER_SECRET = '' # fill in to use yahoo boss search

BING_API_KEY = '' # Fill in to use live bing search

LOG_CONF_PATH = os.path.join(PROJECT_ROOT, 'dev_log_config.yaml')
