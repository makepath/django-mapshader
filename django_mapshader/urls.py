from functools import partial

from django.urls import path

from mapshader import hello
from mapshader.sources import get_services

from django_mapshader import views
from django_mapshader.utils import get_config_file


urlpatterns = []


view_func_creators = {
    'tile': views.get_tile,
    'image': views.get_image,
    'wms': views.get_wms,
    'geojson': views.get_geojson,
}

services = []
for service in get_services(config_path=get_config_file(), contains=None):

    services.append(service)

    view_func = view_func_creators[service.service_type]

    # add operational endpoint
    urlpatterns.append(
        path(
            service.service_url[1:],
            partial(view_func, source=service.source),
            name=f'mapshader-{service.name}'
        )
    )
    urlpatterns.append(
        path(
            service.service_page_url[1:],
            partial(views.service_page, service=service),
            name=f'mapshader-{service.service_page_name}'
        )
    )


urlpatterns.append(
    path(
        '',
        partial(views.index_page, services=services),
        name='mapshader-index'
    )
)
hello(services)