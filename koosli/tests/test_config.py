import os

from koosli.search_providers import bing, yahoo

DEBUG = True

SECRET_KEY = 'not a secret'

SPLASH_REGISTRATION = False

#=========================================
# Search Providers
#=========================================

SEARCH_PROVIDERS = {
    'bing': bing.BingMock,
    'yahoo': yahoo.YahooMock,
}

#=========================================
# Database Config
#=========================================

# In-memory SQLite for quick test runs
SQLALCHEMY_DATABASE_URI = 'sqlite://'
