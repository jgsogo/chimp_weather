#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Observation

class ObservationModelAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'time', '_non_forecast')
    list_filter = ('_non_forecast', 'time',)

admin.site.register(Observation, ObservationModelAdmin)