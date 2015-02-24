#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets

from .models import Observation, Place, SquareArea

class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        return self.model._meta.get_all_field_names()
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            form = self.get_formset(request, obj).form
            fields = form.base_fields.keys()
        return fields


class ObservationModelAdmin(ReadOnlyAdmin):
    list_display = ('longitude', 'latitude', 'time', '_non_forecast')
    list_filter = ('_non_forecast', 'time',)


# Places and Areas
class PlaceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude',)

class SquareAreaModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude_min', 'longitude_max', 'latitude_min', 'latitude_max')

admin.site.register(Observation, ObservationModelAdmin)
admin.site.register(Place, PlaceModelAdmin)
admin.site.register(SquareArea, SquareAreaModelAdmin)