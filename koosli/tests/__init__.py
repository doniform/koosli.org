# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~

    Define TestCase as base class for unit tests.
    Ref: http://packages.python.org/Flask-Testing/
"""
import os

from flask.ext.testing import TestCase as Base

from koosli import create_app, db
from koosli.user import User, UserStats, ADMIN, USER, ACTIVE


class TestCase(Base):
    """Base TestClass for the application."""

    def create_app(self):
        """Create and return a testing flask app."""
        
        test_config = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_config.py'))
        app = create_app(config_file=test_config)
        return app

    def init_data(self):
        """Initialize the databse with dummy users"""

        self.demo = User(
                email=u'demo@example.com',
                password=u'123456',
                role_code=USER,
                status_code=ACTIVE,
                user_stats=UserStats())
        self.admin = User(
                email=u'admin@example.com',
                password=u'123456',
                role_code=ADMIN,
                status_code=ACTIVE,
                user_stats=UserStats())
        db.session.add(self.demo)
        db.session.add(self.admin)
        db.session.commit()

    def setUp(self):
        """Reset all tables before testing."""

        self.client = self.app.test_client()
        db.create_all()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""

        db.drop_all()

    def login(self, username, password):
        data = {
            'email': username,
            'password': password,
        }
        response = self.client.post('/user/login', data=data, follow_redirects=True)
        return response

    def _logout(self):
        response = self.client.get('/user/logout')
        self.assertRedirects(response, location='/')

    def _test_get_request(self, endpoint, template=None, redirect=None):
        """Test a URL with a get request to ensure correct response code"""
        
        response = self.client.get(endpoint)
        if redirect is not None:
            self.assertRedirects(response, location=redirect)
        else:
            self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response