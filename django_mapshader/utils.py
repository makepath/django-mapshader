from django.conf import settings
from os import path

from bokeh.plotting import figure
from bokeh.models.tiles import WMTSTileSource
from bokeh.tile_providers import STAMEN_TONER_BACKGROUND
from bokeh.tile_providers import get_provider
from mapshader.sources import MapService


def get_config_file():
    config_path = settings.MAPSHADER_CONFIG
    if config_path:
        return path.abspath(path.expanduser(config_path))


def build_previewer(service: MapService):
    '''Helper function for creating a simple Bokeh figure with
    a WMTS Tile Source.
    Notes
    -----
    - if you don't supply height / width, stretch_both sizing_mode is used.
    - supply an output_dir to write figure to disk.
    '''

    xmin, ymin, xmax, ymax = service.default_extent

    p = figure(sizing_mode='stretch_both',
               x_range=(xmin, xmax),
               y_range=(ymin, ymax),
               toolbar_location='above',
               tools="pan,wheel_zoom,reset")
    tile_provider = get_provider(STAMEN_TONER_BACKGROUND)
    p.add_tile(tile_provider, alpha=.1)

    p.background_fill_color = 'black'
    p.grid.grid_line_alpha = 0
    p.axis.visible = True

    if service.service_type == 'tile':

        tile_source = WMTSTileSource(url=service.client_url,
                                     min_zoom=0,
                                     max_zoom=15)

        p.add_tile(tile_source, render_parents=False)

    p.axis.visible = False
    return p