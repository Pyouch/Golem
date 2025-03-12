from View import *
from inputs import *
import pygame as pg
from perlin_noise import PerlinNoise
from random import random


def generate_terrain(size, relief=10, octaves=5, seed=None):
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

    heights = generate_terrain(20, seed=random())

    colors = [[Vec(20, 255, 20) for _ in range(len(heights[i]))] for i in range(len(heights))]
    clock = pg.time.Clock()

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
        clock.tick(30)
        nb_times -= 1

    pg.quit()


if __name__ == "__main__":
    run()
