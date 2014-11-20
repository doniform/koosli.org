"""
    This script is used to deploy new code to a server, either it's the production server
    or your local copy of it running in vagrant.

    Execute tasks like this:

        $ fab deploy_vagrant

    This will deploy the code to your local server. (note that you'll have to build it first
    separately!)

    To deploy to the production server (note: you don't need to do this manually, travis does
    it for you):

        $ fab deploy -H <username>@koosli.org

"""

from fabric.api import run, sudo, put, cd, hosts, env, local, lcd
from fabric.context_managers import shell_env
import os
import sys

# Hint about improved color output for windows users
try:
    import colorama
    colorama.init()
except ImportError:
    if sys.platform.startswith('win'):
        print('Colorama not installed!\n\nIf stuff looks weird you might get better results by ' +
            'running `pip install colorama` first. ')


def deploy():
    """ Package the app and push it to a server.

    Assumes the app has already been built (eg `grunt build`).
    """
    # package the static files
    if not os.path.exists('dist'):
        os.mkdir('dist')
    with lcd(os.path.join('koosli', 'static')):
        local('tar czf ../../dist/static-files.tar.gz *')

    # Push the build artifacts to the server
    put('dist/koosli-1.0.0.tar.gz', '/tmp')
    put('dist/static-files.tar.gz', '/tmp')

    # Install the new code
    sudo('/srv/koosli.org/venv/bin/pip install -U /tmp/koosli-1.0.0.tar.gz')
    run('rm /tmp/koosli-1.0.0.tar.gz')

    # Unpack the static files
    sudo('tar xf /tmp/static-files.tar.gz -C /srv/koosli.org/static')
    run('rm /tmp/static-files.tar.gz')

    # Migrate database if changes have been made to schemas
    migrate()

    # Restart the service
    sudo('service uwsgi restart')


@hosts('vagrant@10.10.10.33')
def deploy_vagrant():
    """ Shortcut for deploying to vagrant.

    Basically just an alias for `fab deploy -H vagrant:vagrant@localhost:2222
    """
    env.password = 'vagrant'
    deploy()


def provision():
    if not os.path.exists('dist'):
        os.mkdir('dist')
    local('tar czf dist/salt_and_pillar.tar.gz salt pillar')
    put('dist/salt_and_pillar.tar.gz', '/tmp')
    sudo('tar xf /tmp/salt_and_pillar.tar.gz -C /srv')
    sudo('salt-call state.highstate --force-color --local')
    sudo('rm /tmp/salt_and_pillar.tar.gz')



def migrate():
    """ Apply migration command using Flask-migrate/alembic

    Create new migrations using
        python manage.py db migrate -m 'what has changed'
    """
    with shell_env(KOOSLI_CONFIG_FILE='/srv/koosli.org/prod_settings.py'):
        sudo('/srv/koosli.org/venv/bin/manage.py db upgrade')
