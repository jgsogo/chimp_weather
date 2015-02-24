#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _

from .Observation import make_observation, Observation


class Place(models.Model):
    name = models.CharField(max_length=255)
    comments = models.TextField(blank=True, null=True)

    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        verbose_name = _(u'place')
        verbose_name_plural = _(u'places')

    def make_observation(self, time=None, api_key=None):
        make_observation(self.longitude, self.latitude, time, api_key)

    def observation_set(self):
        return Observation.objects.filter(longitude=self.longitude, latitude=self.latitude)