from flask import Flask, render_template

from koosli.extensions import db, login_manager

# In case of import *
__all__ = ['create_app', 'db']

def create_app(config_file=None):
    app = Flask('koosli')

    configure_application(app, config_file=config_file)
    configure_blueprints(app)
    configure_extensions(app)
    configure_error_handlers(app)

    return app


def configure_application(app, config_file=None):
    """Configure the flask application"""

    if config_file is not None:
        print 'Loading config from %s' % config_file
        app.config.from_pyfile(config_file)
    else:
        print 'Using default config'


def configure_error_handlers(app):
    """Define templates for HMTML error pages"""

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/forbidden.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/not_found.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/server_error.html'), 500


def configure_blueprints(app):
    """Register all application blueprints"""

    from .views import search
    from .views import settings
    from .user import user

    app.register_blueprint(user)
    app.register_blueprint(search.mod)
    app.register_blueprint(settings.mod)


def configure_extensions(app):
    """Configure flask extensions"""

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