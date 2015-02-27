#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import random
import math

from chimp_weather.utils.mesh.tri import TriGrid
from chimp_weather.utils.mesh.point import Point


class TriGridTestCase(unittest.TestCase):
    def setUp(self):
        from chimp_weather.utils.mesh.polygon import Rectangle
        self.square1 = Rectangle(0, 0, 5.5, 3*math.sqrt(3)/2.)
        self.n_sets = 3

    def test_init(self):
        n_vertices = random.randint(4, 1000)
        grid = TriGrid(polygon=self.square1, n_vertices=n_vertices)

        self.assertEqual(self.square1, grid.polygon)
        self.assertEqual(n_vertices, grid._n_vertices)
        self.assertEqual(self.n_sets, grid.n_sets)

    def test_compute(self):
        grid = TriGrid(polygon=self.square1, n_vertices=24)
        grid.compute()
        self.assertEqual(grid.nx, 6)
        self.assertEqual(grid.ny, 4)
        self.assertEqual(grid.side, 1)

    def test_compute_rand(self):
        for i in xrange(100):
            n_vertices = random.randint(4, 1000)
            grid = TriGrid(polygon=self.square1, n_vertices=n_vertices)
            grid.compute()

            self.assertLessEqual(grid.n_vertices, n_vertices)
            self.assertLessEqual(grid.coverage, 1.05)

    def test_grid_vertices(self):
        grid = TriGrid(polygon=self.square1, n_vertices=24)
        grid.compute()

        # Pertenecen al grid
        for y in xrange(4):
            x_offset = 0.0 if y % 2 == 0 else grid.side/2.0
            for x in xrange(6):
                p = Point(x_offset + x*grid.side, y*math.sqrt(3)/2.)
                self.assertEqual(grid.is_grid_vertex(p.x, p.y), True, "Failed with point %s" % p)

    def test_non_grid_vertices(self):
        grid = TriGrid(polygon=self.square1, n_vertices=24)
        grid.compute()

        # No pertenecen al grid
        height = grid.side*math.sqrt(3)/2.0
        for y in xrange(4):
            x_offset = 0.0 if y % 2 == 0 else grid.side/2.0
            for x in xrange(6):
                p = Point(x_offset + x + grid.tolerance*grid.side, y*math.sqrt(3)/2. + grid.tolerance*height)
                self.assertEqual(grid.is_grid_vertex(p.x, p.y), True, "Failed with point %s" % p)
                p = Point(x_offset + x + 1.1*grid.tolerance*grid.side, y*math.sqrt(3)/2.)
                self.assertEqual(grid.is_grid_vertex(p.x, p.y), False, "Failed with point %s" % p)

    def test_neighbours(self):
        n_vertices = 24
        grid = TriGrid(polygon=self.square1, n_vertices=n_vertices)
        grid.compute()

        for i in xrange(100):
            p1 = Point(random.randint(0,10), random.randint(0,10))
            if grid.is_grid_vertex(p1.x, p1.y):
                neighbours = grid.get_neighbours(p1.x, p1.y)
                self.assertEqual(len(neighbours), 2)
                self.assertEqual(sum(len(x) for x in neighbours), 6)
            else:
                neighbours = grid.get_neighbours(p1.x, p1.y)
                self.assertEqual(len(neighbours), 3)
                self.assertEqual(sum(len(x) for x in neighbours), 3)

            for set in neighbours:
                for p in set:
                    self.assertEqual(grid.is_grid_vertex(p.x, p.y), True, "Failed with point %s" % p)
