
from koosli.tests import TestCase



class ErrorTest(TestCase):

    def test_404(self):
        response = self.client.get('/404/')
        self.assert404(response)
        self.assertTemplateUsed('errors/not_found.html')

"""
    def test_403(self):
        response = self.client.get('/404/')
        self.assert404(response)
        self.assertTemplateUsed('errors/page_not_found.html')

    def test_500(self):
        response = self.client.get('/404/')
        self.assert404(response)
        self.assertTemplateUsed('errors/page_not_found.html')
"""