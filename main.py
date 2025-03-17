from View import *
from inputs import *
import pygame as pg
from perlin_noise import PerlinNoise
from time import time
from random import random


def generate_terrain(size, relief=10, octaves=5, seed=None):
    """génère le terrain
    @param size : int, longueur (nombre de case) du côté du terrain
    @param relief: int, hauteur maximale ?, si non précisé vaut 10
    @param octaves: int, ? , si non précisé vaut 5
    @param seed: int, graine de génération,None (1) si non précisé
    @return matrice de terrain : contient la hauteur de chaque case
    """
    if seed is None:
        seed = 1
    noise = PerlinNoise(octaves, seed)
    return [[int(noise((i/size, j/size))*relief) for j in range(size)] + [relief] for i in range(size)] + [[relief] * size]


def run(nb_times=-1):
    inputs = Inputs()
    view = View()

    heights = [[0, 0, 1, 1, 1, 2, 2, 2, 10],
               [0, 1, 1, 1, 1, 1, 2, 2, 10],
               [0, 1, 1, 1, 1, 1, 2, 2, 10],
               [0, 0, 1, 1, 1, 1, 1, 2, 10],
               [0, 0, 1, 1, 1, 1, 1, 1, 10],
               [0, 0, -3, 0, 0, 1, 0, 1, 10],
               [0, 0, 0, 0, 0, 0, 0, 0, 10],
               [10, 10, 10, 10, 10, 10, 10, 10, 10]]

    heights = generate_terrain(100, seed=time())

    colors = [[Vec(20, 255, 20) for _ in range(len(heights[i]))] for i in range(len(heights))]
    clock = pg.time.Clock()

    h = 0
    while not inputs.quit and nb_times != 0:
        view.bg()
        inputs.update()
        view.draw_terrain(heights, colors)
        view.finalize()
        #view.engine.lights[0].pos += Vec(0, 0, 0.01)
        if inputs.holding(pg.K_RIGHT):
            view.engine.lights[0].pos += Vec(0.5, -0.5, 0) * 1/2
        if inputs.holding(pg.K_LEFT):
            view.engine.lights[0].pos += Vec(-0.5, 0.5, 0) * 1/2
        if inputs.holding(pg.K_UP):
            view.engine.lights[0].pos += Vec(-0.5, -0.5, 0) * 1/2
        if inputs.holding(pg.K_DOWN):
            view.engine.lights[0].pos += Vec(0.5, 0.5, 0) * 1/2
        if inputs.holding(pg.K_SPACE):
            view.engine.lights[0].pos += Vec(0, 0, -0.5) * 1/2
        if inputs.holding(pg.K_LSHIFT):
            view.engine.lights[0].pos += Vec(0, 0, 0.5) * 1/2

        """ Pour qu'il suive la souris:
        if inputs.holding(pg.K_UP):
            h += 1/2
        if inputs.holding(pg.K_DOWN):
            h -= 1/2
        view.engine.lights[0].pos = (view.engine.base[0]/40/40 * (inputs.mouse_pos.x - view.screenSize.x/2) +
                                     view.engine.base[1]/40/40 * (inputs.mouse_pos.y - view.screenSize.y/2) +
                                     view.engine.base[2]/40 * h)
        """
        framerate = 1000 / clock.tick(30)
        if inputs.pressed(pg.K_t):
            print(framerate)
        nb_times -= 1

    pg.quit()


if __name__ == "__main__":
    run()
