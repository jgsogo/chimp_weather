#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from chimp_weather.utils.mesh.polygon import Polygon
from chimp_weather.utils.mesh.quad import QuadGrid
from chimp_weather.utils.mesh.tri import TriGrid


class GridManager(models.Manager):
    def create_from_grid(self, grid):
        instance = self.model()
        instance.set_grid(grid)
        return instance


class Grid(models.Model):
    GRID_TYPES = Choices((0, 'quad', _(u'quad')), (1, 'tri', _(u'triangles')))

    # Identificador
    name = models.CharField(max_length=255)
    comments = models.TextField()

    # Configuración de la malla
    _type = models.IntegerField(choices=GRID_TYPES, editable=False)
    _polygon = models.TextField(editable=False)
    _n_vertices = models.PositiveIntegerField(editable=False)

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=True)

    """
    # TODO: Datos para verificar que la creación de la malla es correcta
    nx = test_models.PositiveIntegerField()
    ny = test_models.PositiveIntegerField()
    side = test_models.FloatField()

    # Posicionamiento de la malla
    x_min = test_models.FloatField()
    y_min = test_models.FloatField()
    """

    objects = GridManager()

    class Meta:
        verbose_name = _(u'grid')
        verbose_name_plural = _(u'grids')

    def set_grid(self, grid):
        if self._type != None:
            raise ValueError("It is not allowed to change grid once created")
        if isinstance(grid, QuadGrid):
            self._type = Grid.GRID_TYPES.quad
        elif isinstance(grid, TriGrid):
            self._type = Grid.GRID_TYPES.tri
        else:
            raise AttributeError("Unknown grid type: %s" % grid.__class__)
        self._polygon = Polygon.serialize(grid.polygon.points)
        self._n_vertices = grid._n_vertices

    @property
    def polygon(self):
        if not self._polygon:
            return None
        points = Polygon.deserialize(self._polygon)
        return Polygon(points)

    @property
    def grid(self):
        grid = None
        if self._type == Grid.GRID_TYPES.quad:
            grid = QuadGrid(self.polygon, self._n_vertices)
        elif self._type == Grid.GRID_TYPES.tri:
            grid = TriGrid(self.polygon, self._n_vertices)
        else:
            raise AttributeError("Unknown grid type: %s" % self._type)
        grid.compute()
        return grid

