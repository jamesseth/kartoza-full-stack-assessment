"""Django Data models."""
from django.contrib.gis.db import models


class SpikeyPolygon(models.Model):
    """Database model implementation for SpikeyPolygons data."""

    file_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    geometry = models.PolygonField(blank=True, null=True)

    @classmethod
    def create(cls, file_id, name=None, geometry=None):
        """Create a SpikeyPolygon Model instance."""
        book = cls(file_id=file_id, name=name, geometry=geometry)
        return book
