from flask import Flask

def create_app(config_file):
    app = Flask('koosli')
    print 'Loading config from %s' % config_file
    app.config.from_pyfile(config_file)

    from .views import search
    from .views import settings

    app.register_blueprint(search.mod)
    app.register_blueprint(settings.mod)

    return app
