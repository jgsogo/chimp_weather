#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ObservationBase(models.Model):

    # current vs forecast
    time = models.DateTimeField(help_text=_(u'Time for the observation'))
    observed = models.DateTimeField(help_text=_(u'When the observation was taken (call to API)'))
    _non_forecast = models.BooleanField(default=None)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self._non_forecast = (self.time == self.observed)
        super(ObservationBase, self).save(*args, **kwargs)