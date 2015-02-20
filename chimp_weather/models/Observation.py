#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _

import logging
log = logging.getLogger(__name__)


class ObservationManager(models.Manager):
    def non_forecast(self):
        return self.filter(_non_forecast=True)


class Observation(models.Model):
    # place
    latitude = models.FloatField()
    longitude = models.FloatField()

    # current vs forecast
    #_time = models.IntegerField(help_text=_(u'The UNIX time (that is, seconds since midnight GMT on 1 Jan 1970) at which this data point occurs'))
    time = models.DateTimeField(help_text=_(u'Time for the observation'))
    observed = models.DateTimeField(help_text=_(u'When the observation was taken (call to API)'))
    _non_forecast = models.BooleanField()

    # data-point
    temperature = models.FloatField(_('temperature (ºC)'), default=0)
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

    class Meta:
        verbose_name = _('observation')
        verbose_name_plural = _('observations')
        unique_together = (('latitude', 'longitude', 'time', 'observed'),)

    def save(self, *args, **kwargs):
        self._non_forecast = (self.time == self.observed)
        super(Observation, self).save(*args, **kwargs)

# Credit: http://stackoverflow.com/a/10854034
def roundTime(dt=None, roundTo=60):
    """Round a datetime object to any time laps in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt == None : dt = datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + timedelta(0,rounding-seconds,-dt.microsecond)


def make_observation(latitude, longitude, time=None):
    import os
    import forecastio
    api_key = os.environ['FORECASTIO_API_KEY']
    forecast = forecastio.load_forecast(api_key, latitude, longitude)

    now = roundTime(datetime.now(), roundTo=60*60)

    # TODO: Batch create all this instances.

    # Hourly observations
    byHour = forecast.hourly()
    for data in byHour.data:
        o = Observation(latitude=latitude, longitude=longitude)
        o.observed = now
        o.time = data.time
        # data-point
        fields = [('temperature', u'temperature'),
                 ('ozone', u'ozone'),
                 ('apparent_temperature', u'apparentTemperature'),
                 ('dew_point', u'dewPoint'),
                 ('humidity', u'humidity'),
                 ('cloud_cover', u'cloudCover'),
                 ('pressure', u'pressure'),
                 ('wind_speed', u'windSpeed'),
                 ('wind_bearing', u'windBearing'),
                 ('precip_intensity', u'precipIntensity'),
                 ('precip_probability', u'precipProbability'),
                 ]

        for field in fields:
            try:
                setattr(o, field[0], data.d[field[1]])
            except KeyError as e:
                log.error(str(e))

        o.save()