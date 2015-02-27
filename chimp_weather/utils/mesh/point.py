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
        return sorted(points, key=point_order)


def point_order(lhs, rhs):
    if lhs.x == rhs.x:
        return lhs.y - rhs.y
    return lhs.x - rhs.x