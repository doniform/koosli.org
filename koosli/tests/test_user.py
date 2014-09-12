from werkzeug.urls import url_quote

from koosli import db
from koosli.user import User
from koosli.tests import TestCase


class UserTest(TestCase):

    def test_register(self):
        self._test_get_request('/user/register', 'user_register.html')

        data = {
            'email': 'new_user@example.com',
            'password': '123456',
            'agree': True,
        }

        response = self.client.post('/user/register', data=data, follow_redirects=True)
        assert "Hello" in response.data
        new_user = User.query.filter_by(email=data['email']).first()
        assert new_user is not None

    def test_login(self):
        self._test_get_request('/user/login', 'user_login.html')

    def test_logout(self):
        self.login('demo', '123456')
        self._logout()

    # def test_reset_password(self):
    #     response = self.client.get('/user/reset_password')
    #     self.assert_200(response)

    #     data = {
    #         'email': 'demo@example.com',
    #     }

    #     user = User.query.filter_by(email=data.get('email')).first()
    #     assert user is not None
    #     assert user.activation_key is None

    def test_dash(self):
        self.login('demo', '123456')
        self._test_get_request('/user/', 'user_dash.html')

