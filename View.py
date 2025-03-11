from ViewEngine import *
import pygame as pg



class View:
    def __init__(self):
        self.screenSize = Vec(1100, 700)
        self.screen = pg.display.set_mode(self.screenSize.get())
        self.engine = ViewEngine(self.screen)
        self.engine.add_point_light(Vec(5, 5, -3), Vec(1, 1, 1), 5)
        self.engine.set_light_color(Vec(0.2, 0.2, 0.2))

    def bg(self):
        self.screen.fill(0)

    def draw_point_3d(self, vec, color=Vec(255, 255, 255)):
        pg.draw.circle(self.screen, color.get(), self.engine.to_screen(vec).get(), 3)

    def draw_line_3d(self, v1, v2, color=Vec(255, 255, 255)):
        pg.draw.line(self.screen, color.get(), self.engine.to_screen(v1).get(), self.engine.to_screen(v2).get())

    def draw_quad_3d(self, v1, v2, v3, v4, color=Vec(255, 255, 255), width=0, light=True):
        if light:
            color = self.engine.color((v1+v2+v3+v4)/4, -cross(v2-v1, v3-v1), color)
        pg.draw.polygon(self.screen, color.get(), (
            self.engine.to_screen(v1).get(),
            self.engine.to_screen(v2).get(),
            self.engine.to_screen(v3).get(),
            self.engine.to_screen(v4).get()
        ), width)

    def draw_terrain(self, heights, colors):
        corners = Vec(1, 0), Vec(0, 1)
        for i in (range(len(heights))):
            for j in (range(len(heights[i]))):
                self.engine.add_buffer(quad_hor_3d(Vec(i, j), Vec(i+1, j+1), heights[i][j], colors[i][j]))
                for k in range(len(corners)):
                    if corners[k].x + i < len(heights) and \
                            corners[k].y + j < len(heights[corners[k].x + i]):
                        d = corners[k]["xy0"]
                        for l in range(heights[i][j], heights[corners[k].x + i][corners[k].y + j]):
                            pos = Vec(i, j, l)+d, Vec(i, j, l+1)+d-d["xy"].rotate90()["xy0"]*((-1)**k)
                            self.engine.add_buffer(quad_vert_3d(*pos, color=Vec(97, 74, 52)))

        for light in self.engine.lights:
            self.engine.add_buffer(point_3d(light.pos))

    def finalize(self):
        self.engine.finalize()
        pg.display.flip()
