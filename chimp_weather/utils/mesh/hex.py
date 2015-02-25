#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from chimp_weather.utils.mesh.grid import Grid

import logging
log = logging.getLogger(__name__)


class HexGrid(Grid):
    def _compute(self, n_vertices):
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
        a = math.sqrt(3)*(2*n_vertices-1)
        b = -2*(self.polygon.get_height() + math.sqrt(3)*self.polygon.get_width())
        c = -4*self.polygon.get_width()*self.polygon.get_height()
        fixed_side = (-b + math.sqrt(b*b - 4*a*c))/(2.0*a)

        x = int(round( (2.0*self.polygon.get_width()+fixed_side)/(2.0*fixed_side) ))
        y = int(round( (2.0*self.polygon.get_height() + math.sqrt(3)*fixed_side)/(math.sqrt(3)*fixed_side) ))

        return x, y, fixed_side

    def _get_coverage(self):
        return (self.ny-1)*(self.nx-1)*self.side*self.side*math.sqrt(3)/2.0

    def get_vertices(self, n_sets=3):
        assert n_sets == 3, "Not implemented for other but 3"

        vertices = [[],[],[]]
        for yy in xrange(self.ny):
            i = 0
            y_coord = self.polygon.get_min_y() + yy*self.side*math.sqrt(3)/2.0
            x_offset = 0
            j = 0
            if yy % 2 != 0:
                x_offset = self.side/2.0
                j = 2
            for xx in xrange(self.nx):
                vertices[(j + i)%n_sets].append( (x_offset + self.polygon.get_min_x() + xx*self.side, y_coord))
                i += 1
        return vertices

if __name__ == "__main__":
    # Configure log
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # Example - square
    from chimp_weather.utils.mesh.polygon import Square
    s1 = Square(0, 0, 5, 1.733*2.)

    grid = HexGrid(polygon=s1)
    grid.compute(1000)

    print("\tn_x = %s" % grid.nx)
    print("\tn_y = %s" % grid.ny)
    print("\tn_vertices = %s" % (grid.n_vertices))
    print("\tside = %s" % grid.side)
    print("\tcoverage = %s %%" % grid.coverage)
