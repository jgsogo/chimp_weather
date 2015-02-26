#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import random
import math

from chimp_weather.utils.mesh.segment import Point, do_intersect


class SingleTestCase(unittest.TestCase):
    def do_test(self, p1, q1, p2, q2, same_as_intersection, expected):
        msg = None
        if expected:
            msg = u"%s%s and %s%s intersection expected (same_as_intersection=%s)" % (p1, q1, p2, q2, same_as_intersection)
        else:
            msg = u"%s%s and %s%s intersection NOT expected (same_as_intersection=%s)" % (p1, q1, p2, q2, same_as_intersection)
        self.assertEqual(do_intersect(p1, q1, p2, q2, same_as_intersection), expected, msg)

    def test_single(self):
        p1 = Point(0, 0)
        q1 = Point(10, 0)
        self.do_test(p1, q1, p1,  Point(20,0), False, True)


class SegmentTestCase(unittest.TestCase):

    def do_test(self, p1, q1, p2, q2, same_as_intersection, expected):
        msg = None
        if expected:
            msg = u"%s%s and %s%s intersection expected (same_as_intersection=%s)" % (p1, q1, p2, q2, same_as_intersection)
        else:
            msg = u"%s%s and %s%s intersection NOT expected (same_as_intersection=%s)" % (p1, q1, p2, q2, same_as_intersection)
        self.assertEqual(do_intersect(p1, q1, p2, q2, same_as_intersection), expected, msg)

    def test_no_colineal__no_coincident(self):
        # Caso general:
        #  * no son colineales
        #  * no coincide ninguno de sus puntos
        p1 = Point(0,0)
        q1 = Point(10,10)

        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, Point(0,1), Point(5,1), same_as_intersection, True)
            self.do_test(p1, q1, Point(2,1), Point(5,1), same_as_intersection, False)
            self.do_test(p1, q1, Point(1,2), Point(5,1), same_as_intersection, True)
            self.do_test(p1, q1, Point(5,0), Point(5,10), same_as_intersection, True)
            self.do_test(p1, q1, Point(-1,-2), Point(0,10), same_as_intersection, False)

    def test_no_colineal__point_in(self):
        # Un extremo de un segmento pertenece al otro (o a su prolongación), pero
        #  * no son colineales y
        #  * no coinciden con uno de sus extremos
        p1 = Point(0,0)
        q1 = Point(10,0)
        for same_as_intersection in [True, False]:
            # Si comparten un punto SÍ se considera intersección
            self.do_test(p1, q1, Point(-2,-2), Point(2,2), same_as_intersection, True)
            self.do_test(p1, q1, Point(-2,-2), Point(-1,-1), same_as_intersection, False)
            self.do_test(p1, q1, Point(0,-5), Point(0,5), same_as_intersection, True)
            self.do_test(p1, q1, Point(10,-5), Point(10,1), same_as_intersection, True)
            self.do_test(p1, q1, Point(10,2), Point(10,10), same_as_intersection, False)

    def test_colineal__point_in(self):
        # Un extremo de un segmento pertenece al otro (o su prolongación)
        # * son colineales
        # * ningún punto extremo es coincidente

        # Horizontal
        p1 = Point(0,0)
        q1 = Point(10,0)
        for same_as_intersection in [True, False]:
            # Si comparten un punto SÍ se considera intersección
            self.do_test(p1, q1, Point(5,0),  Point(20,0), same_as_intersection, True)
            self.do_test(p1, q1, Point(12,0),  Point(20,0), same_as_intersection, False)
            self.do_test(p1, q1, Point(-2,0),   Point(20,0), same_as_intersection, True)
            self.do_test(p1, q1, Point(-10,0),  Point(-2,0), same_as_intersection, False)

        # Vertical
        p1 = Point(0,0)
        q1 = Point(0,10)
        for same_as_intersection in [True, False]:
            # Si comparten un punto SÍ se considera intersección
            self.do_test(p1, q1, Point(0,5),  Point(0,20), same_as_intersection, True)
            self.do_test(p1, q1, Point(0,12),  Point(0,20), same_as_intersection, False)
            self.do_test(p1, q1, Point(0,-2),   Point(0,20), same_as_intersection, True)
            self.do_test(p1, q1, Point(0,-10),  Point(0,-2), same_as_intersection, False)

        # Diagonal
        p1 = Point(0,0)
        q1 = Point(10,10)
        for same_as_intersection in [True, False]:
            # Si comparten un punto SÍ se considera intersección
            self.do_test(p1, q1, Point(5,5),  Point(20,20), same_as_intersection, True)
            self.do_test(p1, q1, Point(12,12),  Point(20,20), same_as_intersection, False)
            self.do_test(p1, q1, Point(-2,-2),   Point(20,20), same_as_intersection, True)
            self.do_test(p1, q1, Point(-10,-10),  Point(-2,-2), same_as_intersection, False)

    def test_colineal__point_match__with_intersection(self):
        # Uno de los puntos que definen los extremos de los segmentos coincide
        #  * La intersección es un segmento --> siempre tienen que devolver True

        # Son colineales - horizontal
        p1 = Point(0, 0)
        q1 = Point(10, 0)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, p1,  Point(20,0), same_as_intersection, True)
            self.do_test(p1, q1, p1,  Point(2,0), same_as_intersection, True)

            self.do_test(p1, q1, Point(-2,0), q1, same_as_intersection, True)
            self.do_test(p1, q1, Point(2,0), q1, same_as_intersection, True)

            self.do_test(p1, q1, q1,  Point(5,0), same_as_intersection, True)
            self.do_test(p1, q1, q1,  Point(-2,0), same_as_intersection, True)

        # Son colineales - vertical
        p1 = Point(0, 0)
        q1 = Point(0, 10)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, p1,  Point(0, 20), same_as_intersection, True)
            self.do_test(p1, q1, p1,  Point(0, 2), same_as_intersection, True)

            self.do_test(p1, q1, Point(0, -2), q1, same_as_intersection, True)
            self.do_test(p1, q1, Point(0, 2), q1, same_as_intersection, True)

            self.do_test(p1, q1, q1,  Point(0, 5), same_as_intersection, True)
            self.do_test(p1, q1, q1,  Point(0, -2), same_as_intersection, True)

        # Son colineales - vertical
        p1 = Point(0, 0)
        q1 = Point(10, 10)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, p1,  Point(20, 20), same_as_intersection, True)
            self.do_test(p1, q1, p1,  Point(2, 2), same_as_intersection, True)

            self.do_test(p1, q1, Point(-2, -2), q1, same_as_intersection, True)
            self.do_test(p1, q1, Point(2, 2), q1, same_as_intersection, True)

            self.do_test(p1, q1, q1,  Point(5, 5), same_as_intersection, True)
            self.do_test(p1, q1, q1,  Point(-2, -2), same_as_intersection, True)

    def test_colineal__point_match__only_point(self):
        # Alguno de los puntos que definen los extremos de los segmentos coincide
        #  * La intersección es el punto que coincide --> devuelven True/False según el valor de 'same_as_intersection'

        # Son colineales - horizontal
        p1 = Point(0, 0)
        q1 = Point(10, 0)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, q1,  Point(20,0), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(20,2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(20,-2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(10,2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(10,-2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(5,2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(5,-2), same_as_intersection, same_as_intersection)

            self.do_test(p1, q1, p1,  Point(-5,0), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(-5,2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(-5,-2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(0,2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(0,-2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(5,2), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(5,-2), same_as_intersection, same_as_intersection)

        # Son colineales - vertical
        p1 = Point(0, 0)
        q1 = Point(0, 10)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, q1,  Point(0, 20), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(2, 20), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(-2, 20), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(2, 10), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(-2, 10), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(2, 5), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(-2, 5), same_as_intersection, same_as_intersection)

            self.do_test(p1, q1, p1,  Point(0, -5), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(2, -5), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(-2, -5), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(2, 0), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(-2, 0), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(2, 5), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(-2, 5), same_as_intersection, same_as_intersection)

        # Son colineales - diagonal
        p1 = Point(0, 0)
        q1 = Point(10, 10)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, q1,  Point(20, 20), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(20, 10), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(-20, 10), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, q1,  Point(10, 20), same_as_intersection, same_as_intersection)

            self.do_test(p1, q1, p1,  Point(-5, -5), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(0, -5), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(0, 5), same_as_intersection, same_as_intersection)
            self.do_test(p1, q1, p1,  Point(-2, 0), same_as_intersection, same_as_intersection)

    def test_colineal__coincident(self):
        # Alguno de los puntos que definen los extremos de los segmentos coincide
        #  * La intersección es el punto que coincide --> devuelven True/False según el valor de 'same_as_intersection'

        # Son colineales - horizontal
        p1 = Point(0, 0)
        q1 = Point(10, 0)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, p1, q1, same_as_intersection, True)
            self.do_test(p1, q1, q1, p1, same_as_intersection, True)

        # Son colineales - vertical
        p1 = Point(0, 0)
        q1 = Point(0, 10)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, p1, q1, same_as_intersection, True)
            self.do_test(p1, q1, q1, p1, same_as_intersection, True)

        # Son colineales - diagonal
        p1 = Point(0, 0)
        q1 = Point(10, 10)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, p1, q1, same_as_intersection, True)
            self.do_test(p1, q1, q1, p1, same_as_intersection, True)

        # Son colineales - diagonal
        p1 = Point(0, 0)
        q1 = Point(10, 2)
        for same_as_intersection in [True, False]:
            self.do_test(p1, q1, p1, q1, same_as_intersection, True)
            self.do_test(p1, q1, q1, p1, same_as_intersection, True)

