#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from chimp_weather.utils.mesh.grid import Grid

import logging
log = logging.getLogger(__name__)


class HexGrid(Grid):
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
        #   x*y = n_vertices                <- la suma de puntos tiene que ser la indicada (o inferior)
        #   (x-1)*side + side/2 = width     <- el número de intervalos debe cubrir el ancho total
        #   (y-1)*side*sqrt(3)/2 = height
        #   y tenemos que resolver una ecuación de segundo grado para calcular 'side'
        a = math.sqrt(3)*(2*self._n_vertices-1)
        b = -2*(self.polygon.get_height() + math.sqrt(3)*self.polygon.get_width())
        c = -4*self.polygon.get_width()*self.polygon.get_height()
        fixed_side = round((-b + math.sqrt(b*b - 4*a*c))/(2.0*a), self.float_digits)

        x = int(round( (2.0*self.polygon.get_width()+fixed_side)/(2.0*fixed_side) ))
        y = int(round( (2.0*self.polygon.get_height() + math.sqrt(3)*fixed_side)/(math.sqrt(3)*fixed_side) ))

        return x, y, fixed_side

    def _get_coverage(self):
        return (self.ny-1)*(self.nx-1)*self.side*self.side*math.sqrt(3)/2.0

    def get_vertices(self):
        assert self.n_sets == 3, "Not implemented for other but 3"

        vertices = [[],[],[]]
        for yy in xrange(self.ny):
            i = 0
            y_coord = round(self.polygon.get_min_y() + yy*self.side*math.sqrt(3)/2.0, self.float_digits)
            x_offset = 0
            j = 0
            if yy % 2 != 0:
                x_offset = self.side/2.0
                j = 2
            for xx in xrange(self.nx):
                vertices[(j + i)%self.n_sets].append( (round(x_offset + self.polygon.get_min_x() + xx*self.side, self.float_digits), y_coord))
                i += 1
        return vertices

    def is_grid_vertex(self, px, py):
        height = round(self.side*math.sqrt(3)/2.0, self.float_digits)
        y_slot = 0
        def check_y(y):
            y_slot = int((y - self.polygon.get_min_y())/height)
            r = ((y - self.polygon.get_min_y()) - height*y_slot)
            return r <= self.side*self.tolerance

        def check_x(x):
            x_offset = 0.0 if y_slot % 2 == 0 else self.side/2.0
            d = int((x - self.polygon.get_min_x() + x_offset)/self.side)
            r = ((x - self.polygon.get_min_x() + x_offset) - self.side*d)
            return r <= self.side*self.tolerance

        return check_y(py) and check_x(px)

    def _get_grid_neighbours(self, px, py):
        # When the point belongs to the grid:
        #  * there are 6 neighbours
        #  * neighbours belong to two sets
        h = round(math.sqrt(3)/2.0*self.side, self.float_digits)
        neighbours = [[ (px+self.side, py),
                        (px-self.side/2., py+h),
                        (px-self.side/2., py-h)],
                      [ (px-self.side, py),
                        (px+self.side/2., py+h),
                        (px+self.side/2., py-h)],
                      ]
        return neighbours # Neighbours belongs to two sets

    def _get_grid_closest(self, px, py):
        # When the point do not belong to the grid:
        #  * there are three neighbours
        #  * one in each set
        height = round(self.side*math.sqrt(3)/2.0, self.float_digits)
        dy = int((py - self.polygon.get_min_y())/height)
        ry = ((py - self.polygon.get_min_y()) - height*dy)

        y_slot = int((py - self.polygon.get_min_y())/height)
        x_offset = 0.0 if y_slot % 2 == 0 else self.side/2.0
        dx = int((px - self.polygon.get_min_x() + x_offset)/self.side)
        rx = ((px - self.polygon.get_min_x() + x_offset) - self.side*dx)

        if rx > self.side:
            rx = self.side - rx

        x_min = round(self.polygon.get_min_x() + self.side*dx + x_offset, self.float_digits)
        y_min = round(self.polygon.get_min_y() + height*dy, self.float_digits)

        if ry/rx <= math.sqrt(3): # ry/rx <= tan60
            # Dos vertices debajo || Un vertice encima
            return [[(x_min, y_min)], [(x_min + self.side, y_min)], [(x_min + self.side/2., y_min + height)]]
        else:
            # Un vertice debajo || Dos vertices encima
            return [[(x_min, y_min)], [(x_min - self.side/2., y_min + height)], [(x_min + self.side/2., y_min + height)]]


def run_tests():
    import unittest
    testsuite = unittest.TestLoader().loadTestsFromName('tests.test_hex')
    unittest.TextTestRunner(verbosity=1).run(testsuite)


if __name__ == "__main__":
    # Run tests
    print(u"===========================")
    print(u"Running tests for 'hex.py'")
    print(u"===========================")
    run_tests()

    print("\n\n")
    print(u"===========================")
    print(u"Usage examples")
    print(u"===========================")    # Configure log
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # Example - square
    from chimp_weather.utils.mesh.polygon import Square
    s1 = Square(0, 0, 5, 1.733*2.)

    n_vertices = 1000
    n_sets = 3
    grid = HexGrid(polygon=s1, n_vertices=n_vertices, n_sets=n_sets)
    grid.compute()

    print("\tn_x = %s" % grid.nx)
    print("\tn_y = %s" % grid.ny)
    print("\tn_vertices = %s" % (grid.n_vertices))
    print("\tside = %s" % grid.side)
    print("\tcoverage = %s %%" % grid.coverage)

    p1 = (0, 0)
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