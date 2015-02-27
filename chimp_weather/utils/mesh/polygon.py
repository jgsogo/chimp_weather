#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from chimp_weather.utils.mesh.segment import do_intersect, Point



class Polygon(object):
    """
    Un Polígono es un conjunto de puntos que encierran una región del espacio:
     1. Los lados del polígono se consiguen uniendo dos puntos consecutivos
     2. Ningún punto puede estar repetido (evitamos singularidades innecesarias)
     3. Ningún lado puede cortarse con otro lado
    """
    points = []

    def __init__(self, points):
        Polygon._check_integrity(points)
        self.points = points

    def __eq__(self, other):
        if isinstance(other, Polygon):
            return self.points == other.points
        return NotImplemented

    @classmethod
    def _check_integrity(cls, points):
        # 1. Ningún punto puede estar repetido
        if len(points) != len(set(points)):
            raise ValueError("There is, at least, one point repeated")

        # 2. Ningún lado puede cortarse con otro lado
        sides = []
        for first, second in zip(points, points[1:]+points[:1]):
            sides.append((first, second))

        for pair in itertools.product(sides, repeat=2):
            p1 = Point(*pair[0][0])
            q1 = Point(*pair[0][1])
            p2 = Point(*pair[1][0])
            q2 = Point(*pair[1][1])
            if not p1==p2 or not q1==q2:
                if do_intersect(p1, q1, p2, q2, same_is_intersection=False):
                    print p1, q1, p2, q2
                    raise ValueError("Segments intersects")
        return True

    @property
    def min_x(self):
        if not hasattr(self, '_min_x'):
            setattr(self, '_min_x', min([p[0] for p in self.points]))
        return getattr(self, '_min_x')

    @property
    def min_y(self):
        if not hasattr(self, '_min_y'):
            setattr(self, '_min_y', min([p[1] for p in self.points]))
        return getattr(self, '_min_y')

    @property
    def max_x(self):
        if not hasattr(self, '_max_x'):
            setattr(self, '_max_x', max([p[0] for p in self.points]))
        return getattr(self, '_max_x')

    @property
    def max_y(self):
        if not hasattr(self, '_max_y'):
            setattr(self, '_max_y', max([p[1] for p in self.points]))
        return getattr(self, '_max_y')

    @property
    def width(self):
        return self.max_x - self.min_x

    @property
    def height(self):
        return self.max_y - self.min_y

    def get_area(self):
        raise NotImplementedError()

    def is_inside(self, px, py):
        raise NotImplementedError()

    @classmethod
    def serialize(cls, points):
        return u";".join([u"%s,%s" % (p[0], p[1]) for p in points])

    @classmethod
    def deserialize(cls, string):
        return [tuple(map(float, it.split(u","))) for it in string.split(u";")]


class Rectangle(Polygon):
    def __init__(self, x, y, width, height):
        points = [(x,y), (x+width, y), (x+width, y+height), (x, y+height)]
        super(Rectangle, self).__init__(points)

    def get_area(self):
        return (self.width*self.height)


def run_tests(verbosity=10):
    from chimp_weather.utils.mesh.segment import run_tests as segment_tests
    segment_tests(verbosity)
    print("\n\n")

    print(u"===========================")
    print(u"Running tests for 'polygon.py'")
    print(u"===========================")

    import unittest
    testsuite = unittest.TestLoader().loadTestsFromName('tests.test_polygon')
    unittest.TextTestRunner(verbosity=verbosity).run(testsuite)


if __name__ == "__main__":
    # Run tests
    run_tests()
