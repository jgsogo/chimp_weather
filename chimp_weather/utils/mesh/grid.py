#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chimp_weather.utils.mesh.polygon import Polygon


class Grid(object):
    float_digits = 4 # precision (this should be the same as the ones stored in the database
    tolerance = 0.05 # Tolerancia expresada con relación al tamaño del lado

    def __init__(self, polygon, n_vertices, n_sets):
        assert isinstance(polygon, Polygon)
        self.polygon = polygon
        self._n_vertices = n_vertices
        self.n_sets = n_sets

    def _compute(self):
        raise NotImplementedError()

    def _get_coverage(self):
        raise NotImplementedError()

    def compute(self):
        x, y, self.side = self._compute()
        self.nx, self.ny = self._n_vertices_constraint(self._n_vertices, x, y)

    def get_vertices(self):
        raise NotImplementedError()

    def is_grid_vertex(self, px, py):
        raise NotImplementedError()

    def _get_grid_neighbours(self, px, py):
        raise NotImplementedError()

    def _get_grid_closest(self, px, py):
        raise NotImplementedError

    def get_neighbours(self, px, py):
        if self.is_grid_vertex(px, py):
            return self._get_grid_neighbours(px, py)
        else:
            return self._get_grid_closest(px, py)

    @property
    def n_vertices(self):
        return self.nx*self.ny

    @property
    def coverage(self):
        coverage = self._get_coverage()
        return coverage/float(self.polygon.get_area())

    @classmethod
    def _n_vertices_constraint(cls, n_vertices, x, y):
        while x*y > n_vertices:
            if y > x:
                y = y-1
            elif x > y:
                x = x-1
            else:
                y = y-1 #TODO: Pensar si es adecuado.
        return x, y