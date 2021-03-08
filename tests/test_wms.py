import json

from django.conf import settings
from django.test import TestCase

from .utils import serparete_query_params


class WmsViewTestCase(TestCase):
    wms_services = [
        service for service in settings.SERVICES if service.service_type == 'wms'
    ]

    def test_default_wms_is_working(self):
        for wms in self.wms_services:
            path, query_params = serparete_query_params(wms.default_url)
            response = self.client.get(path, query_params)
            self.assertEqual(response.status_code, 200)

    def test_default_wms_page_is_working(self):
        for wms in self.wms_services:
            response = self.client.get(f'/{wms.key}')
            self.assertEqual(response.status_code, 200)

    def test_legend(self):
        for wms in self.wms_services:
            response = self.client.get(wms.legend_url)
            self.assertEqual(response.status_code, 200)

            data = json.loads(response.json())
            self.assertIsInstance(data, list)
