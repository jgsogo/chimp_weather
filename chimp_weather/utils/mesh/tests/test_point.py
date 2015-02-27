#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import random
import math

from chimp_weather.utils.mesh.point import Point


class PointTestCase(unittest.TestCase):

    def test_basic(self):
        p = Point(1, 2)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)

    def test_equal(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        self.assertEqual(p1, p2)
        self.assertEqual(p1 == p2, True)

        p3 = Point(2, 2)
        self.assertEqual(p1 == p3, False)
        self.assertEqual(p1 != p3, True)

    def test_ordering(self):
        p1 = Point(1, 2)
        p2 = Point(1, 3)
        p3 = Point(2, 1)

        points = [p2, p3, p1]
        ordered = Point.sort(points)

        self.assertEqual(len(ordered), 3)
        self.assertEqual(ordered[0], p1)
        self.assertEqual(ordered[1], p2)
        self.assertEqual(ordered[2], p3)
