#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chimp_weather.utils.mesh.point import Point

import logging
log = logging.getLogger(__name__)


def orientation(p, q, r):
    """
    // To find orientation of ordered triplet (p, q, r).
    // The function returns following values
    // 0 --> p, q and r are colinear
    // 1 --> Clockwise
    // 2 --> Counterclockwise
    """
    val = (q.y - p.y)*(r.x - q.x) - (q.x - p.x)*(r.y - q.y)
    if val == 0:
        return 0 # colinear
    r = 1 if val > 0 else 2
    return r


def on_segment(p, q, r, same_x_is_intersection=True, same_y_is_intersection=True):
    """
    Given three colinear points p, q, r, the function checks if point q lies on line segment 'pr'
    """
    #return q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)
    def lessequal(a, b, same_is_intersection):
        return a <= b if same_is_intersection else a < b

    def moreequal(a, b, same_is_intersection):
        return a >= b if same_is_intersection else a > b

    if  lessequal(q.x, max(p.x, r.x), same_x_is_intersection) \
        and moreequal(q.x, min(p.x, r.x), same_x_is_intersection) \
        and lessequal(q.y, max(p.y, r.y), same_y_is_intersection) \
        and moreequal(q.y, min(p.y, r.y), same_y_is_intersection):
        return True
    return False


def original_do_intersect(p1, q1, p2, q2):
    # Intersección entre dos segmentos p1-q1 y p2-q2
    # Credit: http://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special cases
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if (o1 == 0) and on_segment(p1, p2, q1):
        return True
    # p1, q1 and q2 are colinear and q2 lies on segment p1q1
    if (o2 == 0) and on_segment(p1, q2, q1):
        return True

    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if (o3 == 0) and on_segment(p2, p1, q2):
        return True

    # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if (o4 == 0) and on_segment(p2, q1, q2):
        return True

    return False # Doesn't fall in any of the above cases

def do_intersect(p1, q1, p2, q2, same_is_intersection=True):
    # Casos considerados en el código original
    #   1. (same_is_instersection = True) OR
    #   2. (ningún extremo coincide)
    match1 = (p1 == p2) or (p1 == q2)
    match2 = (q1 == p2) or (q1 == q2)

    # >> Si coinciden ambos hay intersección seguro (salvo caso degenerado donde los segmentos son puntos)
    if match1 and match2:
        return True

    # >> Si hay un 'match' y considero cualquier punto como intersección
    if (match1 or match2) and same_is_intersection:
        return True


    # >> Caso original: funciona correctamente cuando no coincide ningún punto
    ori = original_do_intersect(p1, q1, p2, q2)
    if same_is_intersection or not (match1 or match2):
        return ori

    # >> Capturar falsos positivos -- se ha devuelto que hay intersección porque comparten uno de los puntos
    if ori:
        # same_is_intersection = False
        # match1 or match2 = True
        colineales = (orientation(p1, q1, p2)==0) and (orientation(p1, q1, q2)==0)
        if colineales:
            same_x = p1.x == q1.x
            same_y = p1.y == q1.y
            ori =   on_segment(p1, q2, q1, same_x, same_y) \
                    or on_segment(p1, p2, q1, same_x, same_y) \
                    or on_segment(p2, p1, q2, same_x, same_y) \
                    or on_segment(p2, q1, q2, same_x, same_y)
        else:
            ori = False

    return ori


def run_tests(verbosity=10):
    from chimp_weather.utils.mesh.point import run_tests as point_tests
    point_tests(verbosity)
    print("\n\n")

    print(u"===========================")
    print(u"Running tests for 'segment.py'")
    print(u"===========================")

    import unittest
    #testsuite = unittest.TestLoader().loadTestsFromName('tests.test_segment.SingleTestCase')
    testsuite = unittest.TestLoader().loadTestsFromName('tests.test_segment')
    unittest.TextTestRunner(verbosity=verbosity).run(testsuite)


if __name__ == "__main__":
    # Run tests
    run_tests()
