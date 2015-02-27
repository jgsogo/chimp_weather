#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"(%s, %s)" % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    @classmethod
    def sort(cls, points):
        return sorted(points, cmp=point_order)


def point_order(lhs, rhs):
    if lhs.x == rhs.x:
        return lhs.y - rhs.y
    return lhs.x - rhs.x


def run_tests(verbosity=10):
    print(u"===========================")
    print(u"Running tests for 'point.py'")
    print(u"===========================")

    import unittest
    testsuite = unittest.TestLoader().loadTestsFromName('tests.test_point')
    unittest.TextTestRunner(verbosity=verbosity).run(testsuite)


if __name__ == "__main__":
    # Run tests
    run_tests()
