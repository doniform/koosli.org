# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from koosli import create_app

app = create_app()

from koosli import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)



from koosli.user import User, UserStats, ADMIN, ACTIVE

@manager.command
def create_admin():

    passw = raw_input('Password: ')
    admin = User(
            email=u'admin@koosli.org',
            password=passw,
            role_code=ADMIN,
            status_code=ACTIVE,
            user_stats=UserStats())
    db.session.add(admin)
    db.session.commit()

@manager.command
def clear_database():
    sure1 = raw_input('Are you sure you want to remove all tables from database? (y/n) ')
    if not sure1 == 'y':
        return
    sure2 = raw_input('Are you REALLY sure you want to remove all tables from database? (y/n) ')
    if not sure2 == 'y':
        return
    db.drop_all()

def main():
    manager.run()
