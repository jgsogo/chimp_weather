#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from chimp_weather.utils.mesh.grid import Grid

import logging
log = logging.getLogger(__name__)


class QuadGrid(Grid):
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
        b = -(self.polygon.get_width() + self.polygon.get_height())
        c = -(self.polygon.get_width()*self.polygon.get_height())
        fixed_side = round((-b + math.sqrt(b*b - 4*a*c))/(2.0*a), self.float_digits)
        #side2 = (-b - math.sqrt(b*b - 4*a*c))/2.0

        x = int(round(self.polygon.get_width()/fixed_side + 1))
        y = int(round(self.polygon.get_height()/fixed_side + 1))

        return x, y, fixed_side

    def _get_coverage(self):
        return (self.ny-1)*(self.nx-1)*self.side*self.side

    def get_vertices(self):
        assert self.n_sets == 2, "Not implemented for other but 2"
        j = 0
        vertices = [[],[]]
        for yy in xrange(self.ny):
            i = 0
            y_coord = round(s1.get_min_y() + yy*self.side, self.float_digits)
            for xx in xrange(self.nx):
                vertices[(j + i)%self.n_sets].append( (round(s1.get_min_x() + xx*self.side, self.float_digits), y_coord))
                i += 1
            j += self.n_sets-1
        return vertices

    def is_grid_vertex(self, px, py):
        def check_x(x):
            d = int((x - self.polygon.get_min_x())/self.side)
            r = ((x - self.polygon.get_min_x()) - self.side*d)
            return r <= self.side*self.tolerance or abs(r - self.side*self.tolerance) < self.epsilon

        def check_y(y):
            d = int((y - self.polygon.get_min_y())/self.side)
            r = ((y - self.polygon.get_min_y()) - self.side*d)
            return r <= self.side*self.tolerance or abs(r - self.side*self.tolerance) < self.epsilon

        return check_x(px) and check_y(py)

    def _get_grid_neighbours(self, px, py):
        # When the point belongs to the grid:
        #  * there are 4 neighbours
        #  * all neighbours belong to the 'other' set
        neighbours = [[(px, py+self.side), (px, py-self.side),
                      (px+self.side, py), (px-self.side, py)], ]
        return neighbours

    def _get_grid_closest(self, px, py):
        # When the point do not belong to the grid:
        #  * there are four neighbours
        #  * they belongs to two sets
        dx = int((px - self.polygon.get_min_x())/self.side)
        dy = int((py - self.polygon.get_min_y())/self.side)

        x_min = round(self.polygon.get_min_x() + self.side*dx, self.float_digits)
        y_min = round(self.polygon.get_min_y() + self.side*dy, self.float_digits)
        neighbours = [[(x_min, y_min),
                       (x_min + self.side, y_min + self.side),],
                      [(x_min + self.side, y_min),
                       (x_min, y_min + self.side),]]
        return neighbours


def run_tests():
    import unittest
    testsuite = unittest.TestLoader().loadTestsFromName('tests.test_quad')
    unittest.TextTestRunner(verbosity=1).run(testsuite)


if __name__ == "__main__":
    # Run tests
    print(u"===========================")
    print(u"Running tests for 'quad.py'")
    print(u"===========================")
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
    from chimp_weather.utils.mesh.polygon import Square
    s1 = Square(-5, -5, 20, 10)

    n_vertices = 1000
    n_sets = 2
    grid = QuadGrid(polygon=s1, n_vertices=n_vertices, n_sets=n_sets)
    grid.compute()

    print("\tn_x = %s" % grid.nx)
    print("\tn_y = %s" % grid.ny)
    print("\tn_vertices = %s" % (grid.n_vertices))
    print("\tside = %s" % grid.side)
    print("\tcoverage = %s %%" % grid.coverage)

    p1 = (-5, -5)
    print("\tneighbours of %s" % str(p1))
    i = 0
    for set in grid.get_neighbours(p1[0], p1[1]):
        i += 1
        print("\t\tset %s:" % i)
        for p in set:
            print("\t\t\t%s" % str(p))

    p2 = (2, 1)
    print("\tneighbours of %s" % str(p2))
    i = 0
    for set in grid.get_neighbours(p2[0], p2[1]):
        i += 1
        print("\t\tset %s:" % i)
        for p in set:
            print("\t\t\t%s" % str(p))