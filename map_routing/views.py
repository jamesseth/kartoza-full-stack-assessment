"""Implementation of django views."""
import json
from typing import Any
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

from django.shortcuts import render

from .filters import PolySpikeFilter
from .models import SpikeyPolygons


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
    results = list()
    pollies = SpikeyPolygons.objects.all()
    for poly in pollies:
        results.append(apply_rdp_to_polygon(poly))
    polygons = list()
    for i in results:
        res = []
        for point in i.coords[0]:
            res.append((chunks(point, 2)))
        polygons.append(res)

    return polygons


def render_route(request):
    """Display polygons on map."""
    pollies = get_polygons()
    filtered_polygons = []
    for poly in pollies:
        filtered_polygons.append(PolySpikeFilter(poly).filtered_poly)

    return render(request, 'improved_map.html',
                  dict(polygons=json.dumps(filtered_polygons),
                       map_center=PolySpikeFilter.MAP_CENTER))
