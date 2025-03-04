from ViewEngine import *
import pygame as pg


class Point:
    def __init__(self, pos: Vec, color: Vec):
        self.pos = pos
        self.color = color

    def draw(self, view):
        view.draw_point_3d(self.pos, self.color)


class Quad:
    def __init__(self, v1, v2, v3, v4, color):
        self.corners = v1, v2, v3, v4
        self.color = color

    def draw(self, view):
        view.draw_quad_3d(*self.corners, self.color)



class View:
    def __init__(self):
        self.screenSize = Vec(1100, 700)
        self.screen = pg.display.set_mode(self.screenSize.get())
        self.engine = ViewEngine(self.screenSize)
        self.engine.add_point_light(Vec(5, 5, -3), Vec(1, 1, 1))
        self.engine.set_light_color(Vec(0.2, 0.2, 0.2))
        self.to_draw_buffer = {}

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

    def add_buffer(self, key, elt):
        key = int(key)
        if key not in self.to_draw_buffer:
            self.to_draw_buffer[key] = []
        self.to_draw_buffer[key].append(elt)

    def buffer_point_3d(self, vec, color=Vec(255, 255, 255)):
        self.add_buffer(self.engine.cam_dist(vec), Point(vec, color))

    def buffer_quad_3d(self, v1, v2, v3, v4, color=Vec(255, 255, 255)):
        self.add_buffer(self.engine.cam_dist((v1 + v2 + v3 + v4)/4), Quad(v1, v2, v3, v4, color))

    def buffer_quad_hor_3d(self, a, b, h=None, color=Vec(255, 255, 255)):
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
        self.buffer_quad_3d(v1, v2, v3, v4, color)

    def buffer_quad_vert_3d(self, a, b, color=Vec(255, 255, 255)):
        """ v1 and v2 must be of dimension 3 """
        v1 = a
        v2 = Vec(a.x, a.y, b.z)
        v3 = b
        v4 = Vec(b.x, b.y, a.z)
        self.buffer_quad_3d(v1, v2, v3, v4, color)

    def draw_terrain(self, heights, colors):
        corners = Vec(1, 0), Vec(0, 1)
        for i in (range(len(heights))):
            for j in (range(len(heights[i]))):
                self.buffer_quad_hor_3d(Vec(i, j), Vec(i+1, j+1), heights[i][j], colors[i][j])
                for k in range(len(corners)):
                    if corners[k].x + i < len(heights) and \
                            corners[k].y + j < len(heights[corners[k].x + i]):
                        d = corners[k]["xy0"]
                        for l in range(heights[i][j], heights[corners[k].x + i][corners[k].y + j]):
                            pos = Vec(i, j, l)+d, Vec(i, j, l+1)+d-d["xy"].rotate90()["xy0"]*((-1)**k)
                            self.buffer_quad_vert_3d(*pos, color=Vec(97, 74, 52))

        for light in self.engine.lights:
            self.buffer_point_3d(light.pos)

    def draw_buffer(self):
        keys = list(self.to_draw_buffer.keys())
        keys.sort(reverse=True)
        for h in keys:
            for primitive in self.to_draw_buffer[h]:
                primitive.draw(self)
        self.to_draw_buffer = {}


    def finalize(self):
        self.draw_buffer()
        pg.display.flip()
