
from flask import url_for

from koosli.tests import TestCase



class DecoratorTest(TestCase):

    def test_admin_required(self):
        self.logout()
        response = self.client.get('/admin/')
        print response.data
        self.assertRedirects(response, location=url_for('user.login'))

        self.login(self.demo.email)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed('errors/forbidden.html')

        self.login(self.admin.email)
        response = self.client.get('/admin/')
        self.assert200(response)
