import os

from koosli.search_providers import bing

from config import *


DEBUG = True

SECRET_KEY = 'not a secret'



#=========================================
# Database Config
#=========================================

# Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
SQLALCHEMY_ECHO = True

# SQLITE for prototyping.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT + '/kooslidb.db'

# MYSQL for production.
#SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db?charset=utf8'
