#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import random

from chimp_weather.utils.mesh.quad import QuadGrid


class QuadGridTestCase(unittest.TestCase):
    def setUp(self):
        from chimp_weather.utils.mesh.polygon import Rectangle
        self.square1 = Rectangle(0, 0, 9, 9)

    def test_init(self):
        n_vertices = random.randint(4, 1000)
        n_sets = 2
        grid = QuadGrid(polygon=self.square1, n_vertices=n_vertices, n_sets=n_sets)

        self.assertEqual(self.square1, grid.polygon)
        self.assertEqual(n_vertices, grid._n_vertices)
        self.assertEqual(n_sets, grid.n_sets)

    def test_compute(self):
        grid = QuadGrid(polygon=self.square1, n_vertices=100, n_sets=2)
        grid.compute()

        self.assertEqual(grid.nx, 10)
        self.assertEqual(grid.ny, 10)
        self.assertEqual(grid.side, 1)

    def test_compute_rand(self):
        for i in xrange(100):
            n_vertices = random.randint(4, 1000)
            grid = QuadGrid(polygon=self.square1, n_vertices=n_vertices, n_sets=2)
            grid.compute()

            self.assertLessEqual(grid.n_vertices, n_vertices)
            self.assertLessEqual(grid.coverage, 1.05)

    def test_grid_vertices(self):
        grid = QuadGrid(polygon=self.square1, n_vertices=100, n_sets=2)
        grid.compute()

        # Pertenecen al grid
        for x in xrange(10):
            for y in xrange(10):
                p = (x, y)
                self.assertEqual(grid.is_grid_vertex(p[0], p[1]), True, "Failed with point %s" % str(p))

    def test_non_grid_vertices(self):
        grid = QuadGrid(polygon=self.square1, n_vertices=100, n_sets=2)
        grid.compute()

        # No pertenecen al grid
        for x in xrange(10):
            for y in xrange(10):
                p = (x+grid.tolerance*grid.side, y+grid.tolerance*grid.side)
                self.assertEqual(grid.is_grid_vertex(p[0], p[1]), True, "Failed with point %s" % str(p))
                p = (x+1.1*grid.tolerance, y)
                self.assertEqual(grid.is_grid_vertex(p[0], p[1]), False, "Failed with point %s" % str(p))


    def test_neighbours(self):
        n_vertices = 100
        n_sets = 2
        grid = QuadGrid(polygon=self.square1, n_vertices=n_vertices, n_sets=n_sets)
        grid.compute()

        for i in xrange(100):
            p1 = (random.randint(0,10), random.randint(0,10))
            if grid.is_grid_vertex(p1[0], p1[1]):
                neighbours = grid.get_neighbours(p1[0], p1[1])
                self.assertEqual(len(neighbours), 1)
                self.assertEqual(sum(len(x) for x in neighbours), 4)
            else:
                neighbours = grid.get_neighbours(p1[0], p1[1])
                self.assertEqual(len(neighbours), 2)
                self.assertEqual(sum(len(x) for x in neighbours), 4)

            for set in neighbours:
                for p in set:
                    self.assertEqual(grid.is_grid_vertex(p[0], p[1]), True, "Failed with point %s" % str(p))
