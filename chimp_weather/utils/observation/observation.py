#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from chimp_weather.utils.mesh.point import Point


class ObservationData(Point):
    def __init__(self, longitude, latitude):
        super(ObservationData, self).__init__(x=longitude, y=latitude)

    @property
    def longitude(self):
        return self.x

    @longitude.setter
    def longitude(self, value):
        self.x = value

    @property
    def latitude(self):
        return self.y

    @latitude.setter
    def latitude(self, value):
        self.y = value

    @classmethod
    def round_time(cls, dt=None, roundTo=60):
        # Credit: http://stackoverflow.com/a/10854034
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