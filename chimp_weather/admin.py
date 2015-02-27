#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Grid, GridData


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


class GridModelAdmin(admin.ModelAdmin):
    list_display = ('name', '_type', '_n_vertices')
    list_filter = ('_type',)
    readonly_fields = ('_type', '_n_vertices', '_polygon',)


# Places and Areas
class GridDataModelAdmin(admin.ModelAdmin):
    list_display = ('grid', 'set', 'time', '_non_forecast',)
    list_filter = ('_non_forecast',)


admin.site.register(Grid, GridModelAdmin)
admin.site.register(GridData, GridDataModelAdmin)
