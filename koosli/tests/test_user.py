from werkzeug.urls import url_quote

from flask import url_for, current_app
from flask.ext.login import login_user, current_user

from koosli import db
from koosli.user import User, ADMIN, USER, ACTIVE, USER_ROLE, USER_STATUS
from koosli.tests import TestCase


class UserTest(TestCase):

    def test_register(self):
        self._test_get_request('/user/register', 'user_register.html')

        # Valid data
        data = {
            'email': 'new_user@example.com',
            'password': '123456',
            'confirm': '123456',
            'accept_tos': True,
        }

        response = self.client.post('/user/register', data=data, follow_redirects=True)
        self.assert_200(response)
        new_user = User.query.filter_by(email=data['email']).first()
        self.assertIsNotNone(new_user)
        self.assertTrue(new_user.is_authenticated())

        response = self.client.post('/user/register', data=data, follow_redirects=True)
        self.assertTrue('belongs to a registered user' in response.data)

        # Invalid data
        data_invalid = {
            'email': 'invalid_user.example.com',
            'password': '123456',
            'confirm': '123456',
            'accept_tos': True,
        }

        response = self.client.post('/user/register', data=data_invalid, follow_redirects=True)
        self.assert_200(response)
        invalid_user = User.query.filter_by(email=data_invalid['email']).first()
        self.assertIsNone(invalid_user)



    def test_login(self):
        self._test_get_request('/user/login', 'user_login.html')
        data = {
            'email': 'demo@example.com',
            'password': '123456',
        }
        response = self.client.post('/user/login', data=data, follow_redirects=True)

        invalid_data = {
            'email': 'not_a_user',
            'password': '123456',
        }
        response = self.client.post('/user/login', data=invalid_data, follow_redirects=True)
        self.assert_200(response)
        self.assertTrue('This email does not belong to a registered user' in response.data)



    def test_logout(self):
        self.login(self.demo.email)
        response = self.client.get('/user/logout', follow_redirects=True)
        self.assert_200(response)

    # [TODO] NOT IMPLEMENTED YET
    # def test_reset_password(self):
    #     response = self.client.get('/user/reset_password')
    #     self.assert_200(response)

    #     data = {
    #         'email': 'demo@example.com',
    #     }

    #     user = User.query.filter_by(email=data.get('email')).first()
    #     assert user is not None
    #     assert user.activation_key is None

    def test_index(self):
        self.login(self.demo.email)
        current_app.login_manager.reload_user()
        response = self._test_get_request(url_for('user.index'), 'user_dash.html')
        self.logout()
        self._test_get_request(url_for('user.index'), redirect='/user/login?next=%2Fuser%2F')


    def test_role(self):
        self.assertEqual(self.admin.role, USER_ROLE[ADMIN])
        self.assertEqual(self.demo.role, USER_ROLE[USER])

    def test_check_password(self):
        self.demo.password = 'noqewfoih241'
        self.assertFalse(self.demo.check_password('123456'))

    def test_is_admin(self):
        self.assertTrue(self.admin.is_admin())
        self.assertFalse(self.demo.is_admin())

    def test_status(self):
        self.assertEqual(self.demo.status, USER_STATUS[ACTIVE])

    def test_authenticate(self):
        self.assertTrue(User.authenticate('demo@example.com', '123456')[1])
        self.assertFalse(User.authenticate('demo1@example.com', '123456')[1])

    def test_get_by_id(self):
        self.assertEqual(User.get_by_id(1), self.demo)

    def test_email_taken(self):
        self.assertTrue(User.email_taken('demo@example.com'))
        self.assertFalse(User.email_taken('demo@example.no'))
