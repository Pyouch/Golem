from View import *
from inputs import *


inputs = Inputs()
view = View()

heights = [[0, 0, 1, 1, 1, 2, 3, 4],
           [0, 1, 1, 1, 1, 1, 2, 2],
           [0, 1, 1, 1, 1, 1, 2, 1],
           [0, 0, 1, 1, 1, 1, 1, 2],
           [1, 0, 1, 1, 1, 1, 1, 1],
           [0, 0, 1, 0, 0, 1, 0, 1],
           [0, 0, 0, 0, 0, 0, 0, 0]]


colors = [[Vec(20, 255, 20) for _ in range(len(heights[i]))] for i in range(len(heights))]
clock = pg.time.Clock()

while not inputs.quit:
    view.bg()
    inputs.update()
    view.draw_terrain(heights, colors)
    view.flip()
    view.engine.lights[0].pos += Vec(0, 0, 0.01)
    clock.tick(30)

pg.quit()
