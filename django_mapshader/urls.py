from functools import partial

from django.conf import settings
from django.urls import path
from django.utils.text import slugify

from mapshader.sources import get_services

from django_mapshader import views
from django_mapshader.utils import get_config_file


app_name = 'django_mapshader'
urlpatterns = []


view_func_creators = {
    'tile': views.get_tile,
    'image': views.get_image,
    'wms': views.get_wms,
    'geojson': views.get_geojson,
    'legend': views.get_legend,
}

if settings.SERVICES:
    default_services = settings.SERVICES
else:
    default_services =  get_services(config_path=get_config_file(), contains=None)

services = []
for service in default_services:

    services.append(service)

    view_func = view_func_creators[service.service_type]

    # add operational endpoint
    urlpatterns.append(
        path(
            service.service_url[1:],
            partial(view_func, source=service.source),
            name=slugify(service.name)
        )
    )

    # add legend endpoint
    urlpatterns.append(
        path(
            service.legend_url[1:],
            partial(view_func_creators['legend'], source=service.source),
            name=slugify(service.legend_name)
        )
    )

    # add service page endpoint
    urlpatterns.append(
        path(
            service.service_page_url[1:],
            partial(views.service_page, service=service),
            name=slugify(service.name)+'-page'
        )
    )


urlpatterns.append(
    path(
        '',
        partial(views.index_page, services=services),
        name='mapshader-index'
    )
)
