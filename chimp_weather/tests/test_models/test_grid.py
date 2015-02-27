#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from django.test import TestCase
from chimp_weather.models import Grid
from chimp_weather.utils.mesh.polygon import Polygon, Rectangle
from chimp_weather.utils.mesh.quad import QuadGrid
from chimp_weather.utils.mesh.tri import TriGrid


class GridTestCase(TestCase):
    def setUp(self):
        self.rect1 = Rectangle(0,0, 20, 10)
        self.n_vertices = 100
        self.quad = QuadGrid(self.rect1, self.n_vertices)
        self.tri = TriGrid(self.rect1, self.n_vertices)

    def test_create(self):
        instance = Grid.objects.create_from_grid(self.quad)
        self.assertEqual(instance._type, Grid.GRID_TYPES.quad)
        self.assertEqual(instance.polygon, self.rect1)
        self.assertEqual(instance._n_vertices, self.n_vertices)
        self.assertEqual(instance.n_sets, 2)

        instance2 = Grid.objects.create_from_grid(self.tri)
        self.assertEqual(instance2._type, Grid.GRID_TYPES.tri)
        self.assertEqual(instance2.polygon, self.rect1)
        self.assertEqual(instance2._n_vertices, self.n_vertices)
        self.assertEqual(instance2.n_sets, 3)

    def test_polygon_property(self):
        instance = Grid.objects.create_from_grid(self.quad)
        self.assertEqual(instance.polygon, self.quad.polygon)

        instance2 = Grid.objects.create_from_grid(self.tri)
        self.assertEqual(instance2.polygon, self.tri.polygon)

    def test_grid_property(self):
        instance = Grid.objects.create_from_grid(self.quad)
        self.assertEqual(instance.grid, self.quad)

        instance2 = Grid.objects.create_from_grid(self.tri)
        self.assertEqual(instance2.grid, self.tri)
