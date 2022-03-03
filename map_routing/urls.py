"""Url paths implementations for map routing app."""
from django.urls import path

from . import views
app_name = 'map_routing'

urlpatterns = [
    path('', views.render_route, name='render_route'),
]
