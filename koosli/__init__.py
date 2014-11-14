from flask import Flask, render_template, request, url_for, redirect
from logging import getLogger
import logging.config
import os
import textwrap
import yaml

from koosli.extensions import db, login_manager

# In case of import *
__all__ = ['create_app', 'db']
_logger = getLogger(__name__)

def create_app(config_file=None):
    app = Flask('koosli')

    configure_application(app, config_file=config_file)

    _init_logging(app)

    configure_blueprints(app)
    configure_extensions(app)
    configure_error_handlers(app)
    add_static_redirects(app)

    return app


def configure_application(app, config_file=None):
    '''Configure the flask application'''
    core_config = os.path.abspath(os.path.join(os.path.dirname(__file__), 'core_config.py'))
    app.config.from_pyfile(core_config)

    if config_file is not None:
        print 'Loading config from %s' % config_file
        app.config.from_pyfile(config_file)


def add_static_redirects(app):
    """ Add redirects to known-url files like /robots.txt and /favicon.ico to
    their actual location.
    """
    with app.app_context():
        app.add_url_rule('/robots.txt', 'robots_txt', lambda: redirect(url_for('static', filename='robots.txt')))


def configure_error_handlers(app):
    '''Define templates for HMTML error pages'''

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/forbidden.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/not_found.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        '''Something failed somewhere. Log everything that might come in handy for debugging. '''
        log_generic_error(error)
        return render_template('errors/server_error.html'), 500

    @app.errorhandler(503)
    def backend_error(error):
        log_generic_error(error)
        return render_template('errors/backend_error.html'), 503


def log_generic_error(error):
    log_msg = textwrap.dedent("""Error occured!
        Path:                 %s
        Params:               %s
        HTTP Method:          %s
        Client IP Address:    %s
        User Agent:           %s
        User Platform:        %s
        User Browser:         %s
        User Browser Version: %s
        HTTP Headers:         %s
        Exception:            %s
        """ % (
            request.path,
            request.values,
            request.method,
            request.remote_addr,
            request.user_agent.string,
            request.user_agent.platform,
            request.user_agent.browser,
            request.user_agent.version,
            request.headers,
            error
        )
    )
    _logger.exception(log_msg)



def configure_blueprints(app):
    '''Register all application blueprints'''

    from .views import search
    from .views import settings
    from .user import user
    from .admin import admin

    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(search.mod)
    app.register_blueprint(settings.mod)


def configure_extensions(app):
    '''Configure flask extensions'''

    #=========================================
    # Database management
    #=========================================

    db.init_app(app)

    if app.debug:
        with app.app_context():
            db.create_all()

    #=========================================
    # flask-login
    #=========================================

    login_manager.login_view = 'user.login'
    login_manager.refresh_view = 'user.reauth'

    @login_manager.user_loader
    def load_user(id):
        from user.models import User
        return User.query.get(id)
    login_manager.setup_app(app)


def _init_logging(app):
    '''Configure logging if a `LOG_CONF_PATH` is defined. '''

    # Disable flask logger handling, https://github.com/mitsuhiko/flask/issues/641
    app.logger_name = 'nowhere'
    app.logger

    log_config_dest = app.config.get('LOG_CONF_PATH')
    if log_config_dest:
        print('Loading log config from %s' % log_config_dest)
        with open(log_config_dest) as log_config_file:
            logging.config.dictConfig(yaml.load(log_config_file))
