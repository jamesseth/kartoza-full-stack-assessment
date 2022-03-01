from django.contrib.gis.db import models

class SpikeyPolygons(models.Model):
    fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=-1, blank=True, null=True)
    geometry = models.PolygonField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'spikey_polygons'
