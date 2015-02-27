#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import random
import math

from chimp_weather.utils.mesh.polygon import Polygon, Rectangle


class PolygonTestCase(unittest.TestCase):

    def test_check_integrity(self):
        points = [(0,0), (10,0), (10,10), (0,10)]

        self.assertRaises(ValueError, Polygon._check_integrity, points+[(0,0)])
        self.assertEqual(Polygon._check_integrity(points), True)

    def test_square(self):
        s1 = Rectangle(0, 0, 10, 10)
        self.assertEqual(s1.min_x, 0)
        self.assertEqual(s1.max_x, 10)
        self.assertEqual(s1.min_y, 0)
        self.assertEqual(s1.max_y, 10)
        self.assertEqual(s1.width, 10)
        self.assertEqual(s1.height, 10)
        self.assertEqual(s1.get_area(), 100)

        s2 = Rectangle(-2, 0, 10, 1)
        self.assertEqual(s2.min_x, -2)
        self.assertEqual(s2.max_x, 8)
        self.assertEqual(s2.min_y, 0)
        self.assertEqual(s2.max_y, 1)
        self.assertEqual(s2.width, 10)
        self.assertEqual(s2.height, 1)
        self.assertEqual(s2.get_area(), 10)

    def test_polygon(self):
        points = [(0,0), (10,0), (15, -1), (15, 20)]
        p = Polygon(points)
        self.assertEqual(p.min_x, 0)
        self.assertEqual(p.max_x, 15)
        self.assertEqual(p.min_y, -1)
        self.assertEqual(p.max_y, 20)

    def test_serialization(self):
        points = [(0,0), (-10.1325,0.0), (15.23, -1), (0.15, -0.20)]
        self.assertEqual(points, Polygon.deserialize(Polygon.serialize(points)))