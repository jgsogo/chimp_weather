#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .Observation import make_observation, Observation

import logging
log = logging.getLogger(__name__)


class Area(models.Model):
    name = models.CharField(max_length=255)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = _(u'area')
        verbose_name_plural = _(u'areas')

    def scattered(self, n_points):
        raise RuntimeError('Not implemented')

    def make_observation(self, time=None, api_key=None):
        raise RuntimeError('Not implemented')

    def observation_set(self):
        raise RuntimeError('Not implemented')


class SquareArea(Area):
    longitude_min = models.FloatField()
    longitude_max = models.FloatField()

    latitude_min = models.FloatField()
    latitude_max = models.FloatField()

    n_points = models.SmallIntegerField()

    class Meta:
        verbose_name = _(u"square area")
        verbose_name_plural = _(u"square areas")

    def scattered(self, n_points=None):
        n_points = n_points or self.n_points
        # TODO: Podría ser más adecuado buscar una distribución aleatoria sobre la superficie para evitar puntos singulares (si es que existen)
        ratio = (self.longitude_max-self.longitude_min)/(self.latitude_max-self.latitude_min)
        # Sistema de ecuaciones:
        #   x = ratio*y         <- buscamos la misma proporción que la que tiene el cuadrado
        #   x*y <= n_points    <- la suma de puntos tiene que ser la indicada (o inferior)
        y1 = n_points/(1+ratio)
        x1 = n_points/y1

        y = max(2, int(math.floor(y1)))
        x = max(2, int(math.floor(x1)))

        size_x = (self.longitude_max-self.longitude_min)/float(x-1)
        size_y = (self.latitude_max-self.latitude_min)/float(y-1)

        for xx in xrange(x):
            for yy in xrange(y):
                yield (self.longitude_min + xx*size_x, self.latitude_min + yy*size_y)


    def make_observation(self, n_points=None, time=None, api_key=None):
        points = self.scattered(n_points)
        for point in points:
            make_observation(point[0], point[1])

    def observation_set(self):
        return Observation.objects.filter(longitude__gte=self.longitude_min, longitude__lte=self.longitude_max,
                                          latitude__gte=self.latitude_min, latitude__lte=self.latitude_max)