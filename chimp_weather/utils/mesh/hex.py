#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from chimp_weather.utils.mesh.polygon import Polygon

import logging
log = logging.getLogger(__name__)


def compute_hex_mesh(polygon, n_vertices, fixed_side=None):
    """
    Calcula la cuadrícula HEXAGONAL que mejor se adapta al polígono introducido como parámetro y que tiene un número de
    vértices lo más próximo posible a 'n_vertices'.
    Devuelve una tupla con:
     * número de vértices según la coordenada x
     * número de vértices según la coordenada y
     * longitud del lado
    """
    log.debug(u">> compute_hex_mesh(polygon=%s, n_vertices=%s, fixed_side=%s)" % (type(polygon).__name__, n_vertices, fixed_side))
    assert isinstance(polygon, Polygon)

    if not fixed_side:
        # Compute fixed_length based on 'n_vertices'
        log.debug(u"compute hex grid 'side' with n_vertices=%s" % n_vertices)

        # Sistema de ecuaciones:
        #   x*y = n_vertices                <- la suma de puntos tiene que ser la indicada (o inferior)
        #   (x-1)*side + side/2 = width     <- el número de intervalos debe cubrir el ancho total
        #   (y-1)*side*sqrt(3)/2 = height
        #   y tenemos que resolver una ecuación de segundo grado para calcular 'side'
        a = math.sqrt(3)*(2*n_vertices-1)
        b = -2*(polygon.get_height() + math.sqrt(3)*polygon.get_width())
        c = -4*polygon.get_width()*polygon.get_height()
        fixed_side = (-b + math.sqrt(b*b - 4*a*c))/(2.0*a)
        #side2 = (-b - math.sqrt(b*b - 4*a*c))/2.0
        log.debug(u"fixed_side = %s" % fixed_side)
        return compute_hex_mesh(polygon, n_vertices, fixed_side)

    x = int(round( (2.0*polygon.get_width()+fixed_side)/(2.0*fixed_side) ))
    y = int(round( (2.0*polygon.get_height() + math.sqrt(3)*fixed_side)/(math.sqrt(3)*fixed_side) ))
    return x, y, fixed_side


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

    nx, ny, side = compute_hex_mesh(s1, 9)
    print("\tn_x = %s" % nx)
    print("\tn_y = %s" % ny)
    print("\tside = %s" % side)
    coverage = (ny-1)*(nx-1)*side*side*math.sqrt(3)/2.0*100
    print("\tcoverage = %s %%" % (coverage/float(s1.get_area())))

    n_sets = 3
    j = 0
    vertices = [[],[], []]
    for yy in xrange(ny):
        i = 0
        y_coord = s1.get_min_y() + yy*side*math.sqrt(3)/2.0
        x_offset = 0
        if yy % 2 != 0:
            x_offset = side/2.0
        for xx in xrange(nx):
            vertices[(j + i)%n_sets].append( (x_offset + s1.get_min_x() + xx*side, y_coord))
            i += 1
        j += n_sets-1

    i = 1
    for set in vertices:
        print "---- set %s ----" % i
        print "\n".join([str(p) for p in set])
        i = i + 1

