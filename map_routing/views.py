"""Implementation of django views."""
import json
from typing import Any
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

import geopandas
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from environs import Env

from .filters import PolySpikeFilter
from .models import SpikeyPolygon
# Environs Config
env = Env()
env.read_env()


def chunks(lst: Union[List, Tuple, Set], n: int) -> Union[List, Tuple, Set]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def apply_rdp_to_polygon(poly, tolerance: float = 0.0000000001,
                         preserve_topology: bool = True) -> Any:
    """Reduce data point using RammerDouglasPecker."""
    return(poly.geometry.simplify(tolerance=tolerance,
                                  preserve_topology=preserve_topology))


def get_polygons():
    """
    Get Polygons from Database and split them in to a lost of coordinates.

    :return: A list of lists of lists of tuples.
    """
    pollies = SpikeyPolygon.objects.all()
    polygons = list()
    for poly in pollies:
        polygons.append(dict(file_id=poly.file_id, name=poly.name,
                        coords=poly.geometry.coords))

    return polygons


@require_http_methods(['GET'])
def render_route(request):
    """Display polygons on map."""
    # return render(request, 'improved_map.html',
    #               dict(polygons=None,
    #               map_center=None))
    pollies = get_polygons()
    filtered_polygons = []
    for poly in pollies:
        filtered_polygons.append(
            dict(data=PolySpikeFilter(poly).filtered_poly,
                 file_id=poly['file_id'],
                 name=poly['name']))

    polygons = filtered_polygons if filtered_polygons else {}

    return render(request, 'improved_map.html',
                  dict(polygons=json.dumps(polygons),
                       map_center=PolySpikeFilter.MAP_CENTER))


@require_http_methods(['POST'])
def upload_geopackage(request) -> HttpResponse:
    """Ingest a geopackage file."""
    for filename, file in request.FILES.items():
        output_filename = f'uploaded_{request.FILES[filename]}'
        with open(output_filename, 'wb') as fin:
            fin.write(request.FILES[filename].read())

        gdf = geopandas.read_file(output_filename)
        json_data = json.loads(gdf.to_json())

        for entry in json_data['features']:
            data = {
                'file_id': entry['id'],
                'name': entry.get('properties', '').get('name', ''),
                'geometry': json.dumps(entry.get('geometry', dict()))
            }
            SpikeyPolygon(**data).save()

    return HttpResponse(200)


@require_http_methods('POST')
def export_to_gpkg_file(request):
    """Export a polygon to a geopackage file."""
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    coordinates = []
    for coord in body['geometry']['coordinates']:
        coordinates.append([coord['lat'], coord['lng']])
    body['geometry']['coordinates'] = [coordinates, ]
    new_geojson = dict(
        type='FeatureCollection',
        features=[
            dict(
                id=body['file_id'],
                type='Feature',
                properties=dict(name=body['name']),
                geometry=body['geometry'],
            )])
    gdf = geopandas.GeoDataFrame.from_features(new_geojson['features'])
    gdf.to_file('dataframe.gpkg', driver='GPKG')
    return FileResponse(open('dataframe.gpkg', 'rb'))
