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
        self.points = points

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

    def get_min_x(self):
        raise NotImplementedError()

    def get_min_y(self):
        raise NotImplementedError()

    def get_max_x(self):
        raise NotImplementedError()

    def get_max_y(self):
        raise NotImplementedError()

    def get_width(self):
        raise NotImplementedError()

    def get_height(self):
        raise NotImplementedError()

    def get_area(self):
        raise NotImplementedError()

    def is_inside(self, px, py):
        raise NotImplementedError()

class Square(Polygon):
    x = 0
    y = 0
    width = 1
    height = 1

    def __init__(self, x, y, width, height, *args, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        super(Square, self).__init__(*args, **kwargs)

    def get_min_x(self):
        return self.x

    def get_min_y(self):
        return self.y

    def get_max_x(self):
        return self.x + self.width

    def get_max_y(self):
        return self.y + self.height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

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
