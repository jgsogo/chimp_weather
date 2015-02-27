#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from chimp_weather.models import Grid
from .ObservationBase import ObservationBase



class GridData(ObservationBase):
    serialize = lambda data: u";".join(data)
    deserialize = lambda string: map(float, string.split(u";"))

    grid = models.ForeignKey(Grid)
    set = models.PositiveSmallIntegerField()

    temperature = models.TextField()
    """
    ozone = models.FloatField(blank=True, null=True)
    apparent_temperature = models.FloatField(blank=True, null=True)
    dew_point = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    cloud_cover = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    wind_bearing = models.FloatField(blank=True, null=True)
    precip_intensity = models.FloatField(blank=True, null=True)
    precip_probability = models.FloatField(blank=True, null=True)
    """

    class Meta:
        verbose_name = _(u'grid data')
        verbose_name_plural = _(u'grid data')

    @property
    def points(self):
        return self.grid.get_points(n_set=self.set)

    def set_observations(self, observations):
        # Hay que almacenar las observaciones ¡¡en orden!!
        for o in observations:
            pass


def make_observation(grid, set):
    from chimp_weather.utils.observation.forecastio_observation import ForecastioObservation
    assert isinstance(grid, Grid)

    grid_data = GridData(grid=grid, set=set)
    points = grid_data.points

    observations = {}
    for p in points:
        forecast = ForecastioObservation(p.x, p.y)
        forecast.make_observation()

        for hour,data in forecast.observations.iteritems():
            observations.setdefault(hour, []).append(data)

    observed = datetime.now()

    objects = []
    for time, data in observations.iteritems():
        o = GridData(time=time, observed=observed, grid=grid, set=set)
        temperatures = []
        # Ahora debo obtener las temperaturas en el mismo orden que los puntos
        for obs,check in zip(data, points):
            assert  obs['longitude'] == check.x
            assert  obs['latitude'] == check.y
            temperatures.append(obs['temperature'])
        o.temperature = u";".join(temperatures)