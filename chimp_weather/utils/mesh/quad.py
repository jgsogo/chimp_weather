#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from chimp_weather.utils.mesh.polygon import Polygon

def compute_quad_mesh(polygon, n_vertices, n_sets=2):
    """
    Calcula la cuadrícula que mejor se adapta al polígono introducido como parámetro y que tiene un número de
    vértices lo más próximo posible a 'n_vertices'. Además, los devuelve en 'n_sets' conjuntos de vértices con máxima
    distribución.
    """
    assert isinstance(polygon, Polygon)

    ratio = polygon.get_width()/polygon.get_height()
    # Sistema de ecuaciones:
    #   x = ratio*y         <- buscamos la misma proporción que la que tiene el cuadrado
    #   x*y <= n_points    <- la suma de puntos tiene que ser la indicada (o inferior)
    y = math.sqrt(n_vertices/ratio)
    x = ratio*y

    y = max(2, int(math.floor(y)))
    x = max(2, int(math.floor(x)))

    size_x = (polygon.width)/float(x-1)
    size_y = (polygon.height)/float(y-1)

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


if __name__ == "__main__":
    from chimp_weather.utils.mesh.polygon import Square
    s1 = Square(-10, -10, 20, 10)

    n_sets = 2
    r = compute_quad_mesh(s1, 16, n_sets)

    i = 1
    for set in r:
        print "---- set %s ----" % i
        print "\n".join([str(p) for p in set])
        i = i + 1


