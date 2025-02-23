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

while not inputs.quit:
    inputs.update()
    view.draw_terrain(heights, colors)
    view.flip()

pg.quit()
