from ViewEngine import *
import pygame as pg


class View:
    def __init__(self):
        self.screenSize = Vec(1100, 700)
        self.screen = pg.display.set_mode(self.screenSize.get())
        self.engine = ViewEngine(self.screenSize)
        self.engine.add_point_light(Vec(1, 1, -3), Vec(1, 1, 1))
        self.engine.set_light_color(Vec(0, 0, 0))

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

    def draw_quad_hor_3d(self, a, b, h=None, color=Vec(255, 255, 255), width=0):
        """ v1 and v2 must be of dimension 3 or parameter h filled
        If v1 and v2 have different z, the program will take the v1's z
        """
        assert a.dim() == 2 or h is not None, "v1 must be of dimension 3, or the parameter h must be filled"
        if h is None:
            h = a.z
        v1 = a["xy0"] + Vec(0, 0, h)
        v2 = Vec(b.x, a.y, h)
        v3 = b["xy0"] + Vec(0, 0, h)
        v4 = Vec(a.x, b.y, h)
        self.draw_quad_3d(v1, v2, v3, v4, color, width)

    def draw_quad_vert_3d(self, a, b, color=Vec(255, 255, 255), width=0):
        """ v1 and v2 must be of dimension 3 """
        v1 = a
        v2 = Vec(a.x, a.y, b.z)
        v3 = b
        v4 = Vec(b.x, b.y, a.z)
        self.draw_quad_3d(v1, v2, v3, v4, color, width)

    def draw_terrain(self, heights, colors):
        for light in self.engine.lights:
            self.draw_point_3d(light.pos)
        for i in (range(len(heights))):
            for j in (range(len(heights[i]))):
                self.draw_quad_hor_3d(Vec(i, j), Vec(i+1, j+1), heights[i][j], colors[i][j])

    @staticmethod
    def flip():
        pg.display.flip()
