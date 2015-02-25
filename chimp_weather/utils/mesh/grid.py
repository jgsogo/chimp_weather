#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chimp_weather.utils.mesh.polygon import Polygon


class Grid(object):

    def __init__(self, polygon):
        assert isinstance(polygon, Polygon)
        self.polygon = polygon

    def _compute(self, n_vertices):
        raise NotImplementedError()

    def _get_coverage(self):
        raise NotImplementedError()

    def compute(self, n_vertices):
        x, y, self.side = self._compute(n_vertices)
        self.nx, self.ny = self._n_vertices_constraint(n_vertices, x, y)

    def get_vertices(self, n_sets):
        raise NotImplementedError()

    @property
    def n_vertices(self):
        return self.nx*self.ny

    @property
    def coverage(self):
        coverage = self._get_coverage()
        return coverage/float(self.polygon.get_area())

    def _n_vertices_constraint(self, n_vertices, x, y):
        while x*y > n_vertices:
            if y > x:
                y = y-1
            elif x > y:
                x = x-1
            else:
                y = y-1 #TODO: Pensar si es adecuado.
        return x, y