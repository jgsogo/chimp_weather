#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Polygon(object):

    def get_min_x(self):
        raise NotImplementedError()

    def get_min_y(self):
        raise NotImplementedError()

    def get_max_x(self):
        raise NotImplementedError()

    def get_max_y(self):
        raise NotImplementedError()

    def get_width(self):
        raise NotImplementedError()

    def get_height(self):
        raise NotImplementedError()

    def get_area(self):
        raise NotImplementedError()

    def is_inside(self, px, py):
        raise NotImplementedError()

class Square(Polygon):
    x = 0
    y = 0
    width = 1
    height = 1

    def __init__(self, x, y, width, height, *args, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        super(Square, self).__init__(*args, **kwargs)

    def get_min_x(self):
        return self.x

    def get_min_y(self):
        return self.y

    def get_max_x(self):
        return self.x + self.width

    def get_max_y(self):
        return self.y + self.height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_area(self):
        return (self.width*self.height)