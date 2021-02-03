import sys
import json

from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render

from bokeh.embed import components
from bokeh.resources import INLINE
from mapshader.core import render_map
from mapshader.core import render_geojson
from mapshader.sources import MapSource

from django_mapshader.utils import build_previewer


def index_page(request, services):
    return render(request, 'index.html', context={'service_list': services})


def service_page(request, service: MapSource):
    plot = build_previewer(service)
    script, div = components(dict(preview=plot))
    resources = INLINE.render()
    return render(request, 'service_page.html', context={'service': service,
                                                         'resources': resources,
                                                         'script': script,
                                                         'div': div})


def get_tile(request, source: MapSource, z=0, x=0, y=0):
    if not source.is_loaded:
        print(f'Dynamically Loading Data {source.name}', file=sys.stdout)
        source.load()

    img = render_map(source, x=int(x), y=int(y), z=int(z))
    return StreamingHttpResponse(img.to_bytesio(), content_type='image/png')


def get_image(request, source: MapSource,
              xmin=-20e6, ymin=-20e6,
              xmax=20e6, ymax=20e6,
              height=500, width=500):
    if not source.is_loaded:
        source.load()

    img = render_map(source, xmin=float(xmin), ymin=float(ymin),
                     xmax=float(xmax), ymax=float(ymax),
                     height=int(height), width=int(width))
    return StreamingHttpResponse(img.to_bytesio(), content_type='image/png')


def get_wms(request, source: MapSource,):

    if not source.is_loaded:
        source.load()

    height = request.GET.get('height')
    width = request.GET.get('width')
    bbox = request.GET.get('bbox', '')
    xmin, ymin, xmax, ymax = bbox.split(',')
    img = render_map(source, xmin=float(xmin), ymin=float(ymin),
                     xmax=float(xmax), ymax=float(ymax),
                     height=int(height), width=int(width))
    return StreamingHttpResponse(img.to_bytesio(), content_type='image/png')


def get_geojson(request, source: MapSource):

    if not source.is_loaded:
        source.load()

    response = render_geojson(source)
    return JsonResponse(response, safe=False)
