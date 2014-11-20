# -*- coding: utf-8 -*-

import os
import unittest

from flask.ext.testing import TestCase as Base
from flask.ext.login import login_user, logout_user
from flask import url_for


from koosli import create_app, db
from koosli.user import User, UserStats, ADMIN, USER, ACTIVE


class TestCase(Base):
    '''Base TestClass for the application.'''

    def create_app(self):
        '''Create and return a testing flask app.'''

        test_config = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_config.py'))
        app = create_app(config_file=test_config)
        return app

    def init_data(self):
        '''Initialize the databse with dummy users'''

        self.stats = UserStats()
        self.demo = User(
                email=u'demo@example.com',
                password=u'123456',
                role_code=USER,
                status_code=ACTIVE,
                user_stats = self.stats)
        self.admin = User(
                email=u'admin@example.com',
                password=u'123456',
                role_code=ADMIN,
                status_code=ACTIVE,
                user_stats=UserStats())
        db.session.add(self.stats)
        db.session.add(self.demo)
        db.session.add(self.admin)
        db.session.commit()

    def setUp(self):
        '''Reset all tables before testing.'''

        self.client = self.app.test_client()
        db.create_all()
        self.init_data()

    def tearDown(self):
        '''Clean db session and drop all tables.'''

        db.drop_all()

    def login(self, email):
        """
        logout_user()
        user = User.query.filter_by(email=email).first()
        login_user(user)
        """
        data = {
            'email': email,
            'password': '123456',
        }
        response = self.client.post(url_for('user.login'), data=data, follow_redirects=True)

    def logout(self):
        response = self.client.get(url_for('user.logout'), follow_redirects=True)
        logout_user()

    def _test_get_request(self, endpoint, template=None, redirect=None):
        '''Test a URL with a get request to ensure correct response code'''

        response = self.client.get(endpoint)
        if redirect is not None:
            self.assertRedirects(response, location=redirect)
        else:
            self.assert200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response


class NonContextualTestCase(unittest.TestCase):

    def setUp(self):
        test_config = os.path.join(os.path.dirname(__file__), 'test_config.py')
        self.app = create_app(test_config)
        self.client = self.app.test_client()
        for helper in (200, 201, 301, 302, 400, 401, 403, 404, 500, 503):
            setattr(self, 'assert%d' % helper, self._assert_status_code(helper))
        with self.app.app_context():
            db.create_all()


    def _assert_status_code(self, code):
        """ Helper to create `self.assertXXX` helpers. """
        def _wrapped(response):
            self.assertEqual(response.status_code, code)
        return _wrapped
