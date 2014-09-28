import os

from koosli.search_providers import bing

DEBUG = True

SECRET_KEY = 'not a secret'

SPLASH_REGISTRATION = False

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

# In-memory SQLite for quick test runs
SQLALCHEMY_DATABASE_URI = 'sqlite://'
