import json
import re
import statistics
from collections import namedtuple
from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import render

from .models import SpikeyPolygons


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def apply_rdp_to_polygon(poly, tolerance=0.0000001, preserve_topology=True):
    return(poly.geometry.simplify(tolerance=tolerance, preserve_topology=preserve_topology))


def split_coords(poly):
    lats = []
    lons = []
    for point in poly:
        for lat, lon in point:
            lats.append(lat)
            lons.append(lon)
    return lats, lons


def join_coords(lats, lons):
    print(zip(lats, lons))
    return list(zip(*[lats, lons]))


def get_difference(numbers, count=1):
    if count > 0:
        count -= 1
        results = []
        for index in range(0, len(numbers) - 1):
            results.append(numbers[index + 1] - numbers[index])

        return get_difference(results, count)


def interpolate_coords(coords):
    previous_number = None
    spike_found = False
    spike_index = None

    while 270.0 in coords:
        print('270.0 found in coords')
        for index, value in enumerate(coords):
            if value != 270.0 and spike_found is False:
                print(f'prev number: {value}')
                previous_number = value
            elif value == 270.0 and spike_found is False:
                print(f'spike: {value}')
                spike_found = True
                spike_index = index

            elif value != 270.0 and spike_found is True:
                print(f'after spike {spike_index}: {value}')

                coords[spike_index] = (value + previous_number) / 2
                print(f'New value {coords[spike_index]}')
                previous_number = None
                spike_found = False
                spike_index = None
                break
    return coords


def filter_by_stddev(numbers, tolerance=1.2):

    curr_stdev = statistics.stdev(numbers)

    results = []
    for index in range(0, len(numbers)-1):
        if curr_stdev * -tolerance <= numbers[index] - numbers[index + 1] <= curr_stdev * tolerance:
            results.append(numbers[index])
        else:
            results.append(270.0)

    return interpolate_coords(results)


def get_polygons():
    from pprint import pprint
    results = list()
    pollies = SpikeyPolygons.objects.all()
    for poly in pollies:
        results.append(apply_rdp_to_polygon(poly))
    polygons = list()
    for i in results:
        res = []
        for point in i.coords[0]:
            print(point[0])
            print(point[1])
            res.append((chunks(point, 2)))
        polygons.append(res)

    return polygons


BASE_DIR = Path(__file__).resolve().parent
# Create your views here.


def render_route(request):
    # return HttpResponse("Hello")
    pollies = get_polygons()
    results = []
    for poly in pollies:
        lat_coords, lon_coords = split_coords(poly)
        lat_coords = filter_by_stddev(lat_coords)
        lon_coords = filter_by_stddev(lon_coords)
        poly = join_coords(lon_coords, lat_coords)

        results.append(poly)

    return render(request, 'map.html', dict(polygons=results))
