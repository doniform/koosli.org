from flask import Flask

def create_app(config_file=None):
    app = Flask('koosli')
    if config_file:
        print 'Loading config from %s' % config_file
        app.config.from_pyfile(config_file)

    from .views import search

    app.register_blueprint(search.mod)

    return app
