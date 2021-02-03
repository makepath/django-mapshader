from django.conf import settings
from django.test import TestCase


class ImageViewTestCase(TestCase):
    image_services = [
        service for service in settings.SERVICES if service.service_type == 'image'
    ]

    def test_default_image_is_working(self):
        for image in self.image_services:
            response = self.client.get(image.default_url)
            self.assertEqual(response.status_code, 200)

    def test_default_image_page_is_working(self):
        for image in self.image_services:
            response = self.client.get(f'/{image.key}')
            self.assertEqual(response.status_code, 200)
