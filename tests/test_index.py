import json

from django.conf import settings
from django.test import TestCase
from django.utils.text import slugify


class IndexPageTestCase(TestCase):
    services = [
        service for service in settings.SERVICES
    ]

    def test_index_page_is_working(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_index_page_is_showing_links(self):
        response = self.client.get('')
        html = str(response.content)
        for service in self.services:
            self.assertIn(
                '<a href="' + service.service_page_url + '"',
                html
            )
