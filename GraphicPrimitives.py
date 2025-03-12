import pygame as pg
from Vec import *


class GraphicPrimitives:
    def __init__(self, screen):
        self.screen = screen

    def draw(self, primitive):
        primitive.draw(self.screen)


class Point2D:
    def __init__(self, pos, color=Vec(255, 255, 255)):
        self.pos = pos
        self.color = color

    def draw(self, screen):
        pg.draw.circle(screen, self.color.get(), self.pos.get(), 3)


class Quad2D:
    def __init__(self, p1, p2, p3, p4, color=Vec(255, 255, 255)):
        self.v1 = p1
        self.v2 = p2
        self.v3 = p3
        self.v4 = p4
        self.color = color

    def draw(self, screen):
        pg.draw.polygon(screen, self.color.get(), (self.v1.get(), self.v2.get(), self.v3.get(), self.v4.get()))
