import os

from koosli.search_providers import bing


PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True

SECRET_KEY = 'sdfkljh2q3khwdkefvhoq8w23r0sdc09'


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
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/kooslidb.db'

# MYSQL for production.
#SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db?charset=utf8'