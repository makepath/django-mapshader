from django.conf import settings
from django.test import TestCase


class TileViewTestCase(TestCase):
    tile_services = [
        service for service in settings.SERVICES if service.service_type == 'tile'
    ]

    def test_default_tiles_is_working(self):
        for tiles in self.tile_services:
            response = self.client.get(tiles.default_url)
            self.assertEqual(response.status_code, 200)

    def test_default_tiles_page_is_working(self):
        for tiles in self.tile_services:
            response = self.client.get(f'/{tiles.key}')
            self.assertEqual(response.status_code, 200)
