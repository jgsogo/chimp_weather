#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from chimp_weather.utils.mesh.grid import Grid
from chimp_weather.utils.mesh.point import Point

import logging
log = logging.getLogger(__name__)


class QuadGrid(Grid):
    def __init__(self, polygon, n_vertices):
        super(QuadGrid, self).__init__(polygon, n_vertices, 2)

    def _compute(self):
        """
        Calcula la cuadrícula HEXAGONAL que mejor se adapta al polígono introducido como parámetro y que tiene un número de
        vértices lo más próximo posible a 'n_vertices'.
        Devuelve una tupla con:
         * número de vértices según la coordenada x
         * número de vértices según la coordenada y
         * longitud del lado
        """

        # Sistema de ecuaciones:
        #   x*y = n_vertices        <- la suma de puntos tiene que ser la indicada (o inferior)
        #   (x-1)*side = width      <- el número de intervalos debe cubrir el ancho total
        #   (y-1)*side = height
        #   y tenemos que resolver una ecuación de segundo grado para calcular 'side'
        a = self._n_vertices-1
        b = -(self.polygon.width + self.polygon.height)
        c = -(self.polygon.width*self.polygon.height)
        fixed_side = round((-b + math.sqrt(b*b - 4*a*c))/(2.0*a), self.float_digits)
        #side2 = (-b - math.sqrt(b*b - 4*a*c))/2.0

        x = int(round(self.polygon.width/fixed_side + 1))
        y = int(round(self.polygon.height/fixed_side + 1))

        return x, y, fixed_side

    def _get_coverage(self):
        return (self.ny-1)*(self.nx-1)*self.side*self.side

    def get_vertices(self):
        assert self.n_sets == 2, "Not implemented for other but 2"
        j = 0
        vertices = [[],[]]
        for yy in xrange(self.ny):
            i = 0
            y_coord = round(s1.min_y + yy*self.side, self.float_digits)
            for xx in xrange(self.nx):
                vertices[(j + i)%self.n_sets].append( Point(round(s1.min_x + xx*self.side, self.float_digits), y_coord))
                i += 1
            j += self.n_sets-1
        return vertices

    def is_grid_vertex(self, px, py):
        def check_x(x):
            d = int((x - self.polygon.min_x)/self.side)
            r = ((x - self.polygon.min_x) - self.side*d)
            return r <= self.side*self.tolerance or abs(r - self.side*self.tolerance) < self.epsilon

        def check_y(y):
            d = int((y - self.polygon.min_y)/self.side)
            r = ((y - self.polygon.min_y) - self.side*d)
            return r <= self.side*self.tolerance or abs(r - self.side*self.tolerance) < self.epsilon

        return check_x(px) and check_y(py)

    def _get_grid_neighbours(self, px, py):
        # When the point belongs to the grid:
        #  * there are 4 neighbours
        #  * all neighbours belong to the 'other' set
        neighbours = [[Point(px, py+self.side), Point(px, py-self.side),
                      Point(px+self.side, py), Point(px-self.side, py)], ]
        return neighbours

    def _get_grid_closest(self, px, py):
        # When the point do not belong to the grid:
        #  * there are four neighbours
        #  * they belongs to two sets
        dx = int((px - self.polygon.min_x)/self.side)
        dy = int((py - self.polygon.min_y)/self.side)

        x_min = round(self.polygon.min_x + self.side*dx, self.float_digits)
        y_min = round(self.polygon.min_y + self.side*dy, self.float_digits)
        neighbours = [[Point(x_min, y_min),
                       Point(x_min + self.side, y_min + self.side),],
                      [Point(x_min + self.side, y_min),
                       Point(x_min, y_min + self.side),]]
        return neighbours


def run_tests(verbosity=10):
    from chimp_weather.utils.mesh.grid import run_tests as grid_tests
    grid_tests(verbosity)
    print("\n\n")

    print(u"===========================")
    print(u"Running tests for 'quad.py'")
    print(u"===========================")

    import unittest
    testsuite = unittest.TestLoader().loadTestsFromName('tests.test_quad')
    unittest.TextTestRunner(verbosity=verbosity).run(testsuite)


if __name__ == "__main__":
    # Run tests
    run_tests()

    # Configure log
    log.setLevel(logging.ERROR)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    print("\n\n")
    print(u"===========================")
    print(u"Usage examples")
    print(u"===========================")
    # Example - square
    from chimp_weather.utils.mesh.polygon import Rectangle
    s1 = Rectangle(-5, -5, 20, 10)

    n_vertices = 1000
    grid = QuadGrid(polygon=s1, n_vertices=n_vertices)
    grid.compute()

    print("\tn_x = %s" % grid.nx)
    print("\tn_y = %s" % grid.ny)
    print("\tn_vertices = %s" % (grid.n_vertices))
    print("\tside = %s" % grid.side)
    print("\tcoverage = %s %%" % grid.coverage)

    p1 = Point(-5, -5)
    print("\tneighbours of %s" % p1)
    i = 0
    for set in grid.get_neighbours(p1.x, p1.y):
        i += 1
        print("\t\tset %s:" % i)
        for p in set:
            print("\t\t\t%s" % p)

    p2 = Point(2, 1)
    print("\tneighbours of %s" % p2)
    i = 0
    for set in grid.get_neighbours(p2.x, p2.y):
        i += 1
        print("\t\tset %s:" % i)
        for p in set:
            print("\t\t\t%s" % p)