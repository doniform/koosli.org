
from koosli.tests import TestCase



class ErrorTest(TestCase):

    def test_404(self):
        response = self.client.get('/404/')
        self.assert404(response)
        self.assertTemplateUsed('errors/not_found.html')

    def test_403(self):
        self.login(self.demo.email)
        response = self.client.get('/admin/')
        self.assert403(response)
        self.assertTemplateUsed('errors/forbidden.html')

    # [TODO] How to test for this?
    # def test_500(self):
    #     response = self.client.get('/?')
    #     self.assertEqual(response.status_code, 500)
    #     self.assertTemplateUsed('errors/server_error.html')
