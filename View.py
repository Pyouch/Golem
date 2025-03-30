from ViewEngine import *
import pygame as pg


class View:
    CHUNK_SIZE = 10

    def __init__(self, heights, colors):
        self.screenSize = Vec(1100, 700)
        self.screen = pg.display.set_mode(list(self.screenSize.get()))
        self.engine = ViewEngine(self.screen)
        self.engine.add_point_light(Vec(5, 5, -3), Vec(1, 1, 1), 5)
        self.engine.set_light_color(Vec(0.2, 0.2, 0.2))
        self.terrain = self.terrain_model(heights, colors)

    def bg(self):
        """ Fill the screen in black """
        self.screen.fill(0)

    def terrain_model(self, heights, colors):
        """ Create a model 3D representing the terrain"""
        terrain = Model3D()
        chunks = [[Model3D() for _ in range(len(heights[0]) // self.CHUNK_SIZE + 1)]
                  for _ in range(len(heights) // self.CHUNK_SIZE + 1)]
        corners = Vec(1, 0), Vec(0, 1)
        for i in (range(len(heights))):
            for j in (range(len(heights[i]))):
                c = chunks[i//self.CHUNK_SIZE][j//self.CHUNK_SIZE]
                c.add(quad_hor_3d(Vec(i, j), Vec(i + 1, j + 1), heights[i][j], colors[i][j]))
                for k in range(len(corners)):
                    if corners[k].x + i < len(heights) and \
                            corners[k].y + j < len(heights[corners[k].x + i]):
                        d = corners[k].add_dim()
                        for l in range(heights[i][j], heights[corners[k].x + i][corners[k].y + j]):
                            pos = Vec(i, j, l) + d, Vec(i, j, l + 1) + d - d.remove_dim().rotate90().add_dim() * (
                                        (-1) ** k)
                            c.add(quad_vert_3d(*pos, color=Vec(97, 74, 52)))
        for i in range(len(chunks)):
            for j in range(len(chunks[i])):
                terrain.add(chunks[i][j])
        terrain.finalize()
        return terrain

    def draw_terrain(self):
        """ Draw a terrain described by the relief of the terrain and the colors of the cases """
        self.engine.add_buffer(self.terrain)
        for light in self.engine.lights:
            self.engine.add_buffer(point_3d(light.pos))

    def draw_quad(self, v1: Vec, v2: Vec, v3: Vec, v4: Vec, color=Vec(255, 255, 255)):
        """ Draw a quad """
        self.engine.add_buffer(Quad3D(v1, v2, v3, v4, color))

    def draw_quad_hor(self, a: Vec, b: Vec, h=None, color=Vec(255, 255, 255)):
        """ Draw a horizontal quad """
        self.engine.add_buffer(quad_hor_3d(a, b, h, color))

    def draw_quad_vert(self, a: Vec, b: Vec, color=Vec(255, 255, 255)):
        """ Draw a vertical quad """
        self.engine.add_buffer(quad_vert_3d(a, b, color))

    def draw_point(self, pos: Vec, color=Vec(255, 255, 255)):
        """ Draw a point """
        self.engine.add_buffer(Point3D(pos, color))

    def finalize(self):
        """ Draw on the screen """
        self.engine.finalize()
        pg.display.flip()
