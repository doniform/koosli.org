import os

from koosli.search_providers import bing

DEBUG = True

SECRET_KEY = 'not a secret'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
SQLALCHEMY_ECHO = True

# SQLITE for prototyping.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT + '/kooslidb.db'
