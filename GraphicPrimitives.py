import pygame as pg
from Vec import *


class Primitive2D:
    def draw(self, screen) -> None:
        pass

    def complete(self, vertices, colors) -> None:
        pass


class Point2D(Primitive2D):
    def __init__(self, pos, color=Vec(255, 255, 255)):
        self.pos = pos
        self.color = color

    def draw(self, screen):
        pg.draw.circle(screen, self.color.get(), self.pos.get(), 3)

    def complete(self, vertices, colors) -> None:
        self.pos = vertices[self.pos]


class Quad2D(Primitive2D):
    def __init__(self, p1, p2, p3, p4, color=Vec(255, 255, 255)):
        self.v1 = p1
        self.v2 = p2
        self.v3 = p3
        self.v4 = p4
        self.color = color

    def draw(self, screen):
        pg.draw.polygon(screen, self.color.get(), (self.v1.get(), self.v2.get(), self.v3.get(), self.v4.get()))

    def complete(self, vertices, colors) -> None:
        self.v1 = vertices[self.v1]
        self.v2 = vertices[self.v2]
        self.v3 = vertices[self.v3]
        self.v4 = vertices[self.v4]
        self.color = colors[self.color]


class Container(Primitive2D):
    def __init__(self, primitives: list[Primitive2D] = None):
        if primitives is None:
            self.primitives: list[Primitive2D] = []
        else:
            self.primitives: list[Primitive2D] = primitives

    def add(self, primitive: Primitive2D):
        self.primitives.append(primitive)

    def draw(self, screen):
        for primitive in self.primitives:
            primitive.draw(screen)

    def complete(self, vertices, colors) -> None:
        for primitive in self.primitives:
            primitive.complete(vertices, colors)
