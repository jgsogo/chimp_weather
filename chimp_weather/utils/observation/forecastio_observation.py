#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import forecastio
from datetime import datetime
from chimp_weather.utils.observation.observation import ObservationData, Point


class ForecastioObservation(ObservationData):
    observations = {}
    #observed = None

    # data-point from ForecastIO
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

    def __init__(self, longitude, latitude):
        super(ForecastioObservation, self).__init__(longitude=longitude, latitude=latitude)

    def make_observation(self, api_key=None):
        api_key = api_key or os.environ['FORECASTIO_API_KEY']
        forecast = forecastio.load_forecast(api_key, self.longitude, self.latitude)

        #self.observed = self.round_time(datetime.now(), roundTo=60*60)
        self.observations.clear()
        # Hourly observations
        byHour = forecast.hourly()
        for data in byHour.data:
            observation = {'time': data.time,
                           'longitude': self.longitude,
                           'latitude': self.latitude,
                           'point': Point(self.x, self.y)
                            }
            for field in self.fields:
                observation[field[0]] = data.d[field[1]]
            self.observations[data.time] = observation
