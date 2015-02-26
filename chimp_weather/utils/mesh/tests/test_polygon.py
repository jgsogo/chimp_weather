#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import random
import math

from chimp_weather.utils.mesh.polygon import Polygon


class PolygonTestCase(unittest.TestCase):

    def test_check_integrity(self):
        points = [(0,0), (10,0), (10,10), (0,10)]

        self.assertRaises(ValueError, Polygon._check_integrity, points+[(0,0)])
        self.assertEqual(Polygon._check_integrity(points), True)