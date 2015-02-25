#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from chimp_weather.utils.mesh.polygon import Polygon
from chimp_weather.utils.mesh.grid import Grid

import logging
log = logging.getLogger(__name__)



class QuadGrid(Grid):
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
        #   x*y = n_vertices        <- la suma de puntos tiene que ser la indicada (o inferior)
        #   (x-1)*side = width      <- el número de intervalos debe cubrir el ancho total
        #   (y-1)*side = height
        #   y tenemos que resolver una ecuación de segundo grado para calcular 'side'
        a = n_vertices-1
        b = -(self.polygon.get_width() + self.polygon.get_height())
        c = -(self.polygon.get_width()*self.polygon.get_height())
        fixed_side = (-b + math.sqrt(b*b - 4*a*c))/(2.0*a)
        #side2 = (-b - math.sqrt(b*b - 4*a*c))/2.0
        log.debug(u"fixed_side = %s" % fixed_side)

        x = int(round(self.polygon.get_width()/fixed_side + 1))
        y = int(round(self.polygon.get_height()/fixed_side + 1))

        return x, y, fixed_side

    def _get_coverage(self):
        return (self.ny-1)*(self.nx-1)*self.side*self.side



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
    s1 = Square(-5, -5, 20, 10)

    grid = QuadGrid(polygon=s1)
    grid.compute(1000)

    print("\tn_x = %s" % grid.nx)
    print("\tn_y = %s" % grid.ny)
    print("\tn_vertices = %s" % (grid.n_vertices))
    print("\tside = %s" % grid.side)
    print("\tcoverage = %s %%" % grid.coverage)

    """
    n_sets = 2
    j = 0
    vertices = [[],[]]
    for yy in xrange(ny):
        i = 0
        y_coord = s1.get_min_y() + yy*side
        for xx in xrange(nx):
            vertices[(j + i)%n_sets].append( (s1.get_min_x() + xx*side, y_coord))
            i += 1
        j += n_sets-1

    i = 1
    for set in vertices:
        print "---- set %s ----" % i
        print "\n".join([str(p) for p in set])
        i = i + 1
    """

