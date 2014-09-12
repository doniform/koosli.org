
from koosli.tests import TestCase

class SettingsTest(TestCase):

    def test_main_settings_page(self):
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, 200)
