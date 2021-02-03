from django.conf import settings
from django.test import TestCase


class GeoJsonViewTestCase(TestCase):
    geojson_services = [
        service for service in settings.SERVICES if service.service_type == 'geojson'
    ]

    def test_default_geojson_is_working(self):
        for geojson in self.geojson_services:
            response = self.client.get(geojson.default_url)
            self.assertEqual(response.status_code, 200)

    def test_default_geojson_page_is_working(self):
        for geojson in self.geojson_services:
            response = self.client.get(geojson.service_url)
            self.assertEqual(response.status_code, 200)

    def test_default_geojson_returning_json(self):
        for geojson in self.geojson_services:
            response = self.client.get(geojson.default_url)
            self.assertTrue(len(response.json()) > 1)
