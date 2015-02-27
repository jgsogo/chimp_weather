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
    longitude = models.FloatField()
    latitude = models.FloatField()

    # current vs forecast
    #_time = test_models.IntegerField(help_text=_(u'The UNIX time (that is, seconds since midnight GMT on 1 Jan 1970) at which this data point occurs'))
    time = models.DateTimeField(help_text=_(u'Time for the observation'))
    observed = models.DateTimeField(help_text=_(u'When the observation was taken (call to API)'))
    _non_forecast = models.BooleanField(default=None)

    # data-point
    temperature = models.FloatField(_(u'temperature (ºC)'), default=0)
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
        verbose_name = _(u'observation')
        verbose_name_plural = _(u'observations')
        unique_together = (('longitude', 'latitude', 'time', 'observed'),)

    def save(self, *args, **kwargs):
        self._non_forecast = (self.time == self.observed)
        super(Observation, self).save(*args, **kwargs)

# Credit: http://stackoverflow.com/a/10854034
def round_time(dt=None, roundTo=60):
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


def make_observation(longitude, latitude, time=None, api_key=None):
    import os
    import forecastio_observation
    api_key = api_key or os.environ['FORECASTIO_API_KEY']
    forecast = forecastio_observation.load_forecast(api_key, longitude, latitude)

    now = round_time(datetime.now(), roundTo=60*60)

    # TODO: Bulk creation of all these instances.

    # Hourly observations
    byHour = forecast.hourly()
    objs = []
    for data in byHour.data:
        o = Observation(longitude=longitude, latitude=latitude)
        o.observed = now
        o.time = data.time
        o._non_forecast = (o.time == o.observed)
        # data-point
        fields = [
                 ('temperature', u'temperature'),
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
        objs.append(o)

    Observation.objects.bulk_create(objs)
