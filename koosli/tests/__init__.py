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

        demo = User(
                email=u'demo@example.com',
                password=u'123456',
                role_code=USER,
                status_code=ACTIVE,
                user_stats=UserStats())
        admin = User(
                email=u'admin@example.com',
                password=u'123456',
                role_code=ADMIN,
                status_code=ACTIVE,
                user_stats=UserStats())
        db.session.add(demo)
        db.session.add(admin)
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
            'login': username,
            'password': password,
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        assert "Hello" in response.data
        return response

    def _logout(self):
        response = self.client.get('/logout')
        self.assertRedirects(response, location='/')

    def _test_get_request(self, endpoint, template=None):
        response = self.client.get(endpoint)
        self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response