#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from chimp_weather.utils.mesh.polygon import Polygon

import logging
log = logging.getLogger(__name__)


def compute_quad_mesh(polygon, n_vertices, fixed_side=None):
    """
    Calcula la cuadrícula CUADRADA que mejor se adapta al polígono introducido como parámetro y que tiene un número de
    vértices lo más próximo posible a 'n_vertices'.
    Devuelve una tupla con:
     * número de vértices según la coordenada x
     * número de vértices según la coordenada y
     * longitud del lado
    """
    log.debug(u">> compute_quad_mesh(polygon=%s, n_vertices=%s, fixed_side=%s)" % (type(polygon).__name__, n_vertices, fixed_side))
    assert isinstance(polygon, Polygon)

    if not fixed_side:
        # Compute fixed_length based on 'n_vertices'
        log.debug(u"compute quad grid square 'side' with n_vertices=%s" % n_vertices)

        # Sistema de ecuaciones:
        #   x*y = n_vertices        <- la suma de puntos tiene que ser la indicada (o inferior)
        #   (x-1)*side = width      <- el número de intervalos debe cubrir el ancho total
        #   (y-1)*side = height
        #   y tenemos que resolver una ecuación de segundo grado para calcular 'side'
        a = n_vertices-1
        b = -(polygon.get_width() + polygon.get_height())
        c = -(polygon.get_width()*polygon.get_height())
        fixed_side = (-b + math.sqrt(b*b - 4*a*c))/(2.0*a)
        #side2 = (-b - math.sqrt(b*b - 4*a*c))/2.0
        log.debug(u"fixed_side = %s" % fixed_side)
        return compute_quad_mesh(polygon, n_vertices, fixed_side)

    x = int(round(polygon.get_width()/fixed_side + 1))
    y = int(round(polygon.get_height()/fixed_side + 1))
    return x, y, fixed_side
    """
    size_x = fixed_side
    size_y = fixed_side

    assert n_sets == 2, u"Esta forma de distribuir los puntos probablemente no sea válida para n_sets != 2"
    i = 0
    vertices = [[],[]]
    for xx in xrange(x):
        for yy in xrange(y):
            vertices[i%n_sets].append( (polygon.get_min_x() + xx*size_x, polygon.get_min_y() + yy*size_y))
            i += 1
        if y % 2 == 0:
            i += 1

    return vertices
    """


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

    nx, ny, side = compute_quad_mesh(s1, 16)
    print("\tn_x = %s" % nx)
    print("\tn_y = %s" % ny)
    print("\tside = %s" % side)
    coverage = (nx-1)*(ny-1)*side*side*100
    print("\tcoverage = %s %%" % (coverage/float(s1.get_area())))

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


