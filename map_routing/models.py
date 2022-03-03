"""Django Data models."""
from django.contrib.gis.db import models


class SpikeyPolygons(models.Model):
    """Database model implementation for SpikeyPolygons data."""

    fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=-1, blank=True, null=True)
    geometry = models.PolygonField(blank=True, null=True)

    class Meta:
        """Meta data for db model."""

        managed = False
        db_table = 'spikey_polygons'
