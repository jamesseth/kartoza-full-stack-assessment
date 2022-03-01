from django.contrib.gis.db import models
from django.db import models
# Create your models here.

class WGS84_Coord():
    def __init__(self, poly):
        self.lat = poly(0)
        self.lon = poly(1)

    def get_lattitude(self):
        return poly
