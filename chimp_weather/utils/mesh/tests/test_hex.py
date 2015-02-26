#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import random

from chimp_weather.utils.mesh.hex import HexGrid


class HexGridTestCase(unittest.TestCase):
    def setUp(self):
        from chimp_weather.utils.mesh.polygon import Square
        self.square1 = Square(0, 0, 9, 9)

    def test_init(self):
        n_vertices = random.randint(4, 1000)
        n_sets = 2
        grid = HexGrid(polygon=self.square1, n_vertices=n_vertices, n_sets=n_sets)

        self.assertEqual(self.square1, grid.polygon)
        self.assertEqual(n_vertices, grid._n_vertices)
        self.assertEqual(n_sets, grid.n_sets)
