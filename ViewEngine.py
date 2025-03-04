from Matrix import *
from Light import *


class ViewEngine:
    base_matrix = Matrix.rotation_z(pi / 4) * Matrix.rotation_x(pi / 4)

    def __init__(self, screen_size):
        self.base = [0, 0, 0]
        self.base[0] = self.base_matrix * Vec(1, 0, 0) * 40
        self.base[1] = self.base_matrix * Vec(0, 1, 0) * 40
        self.base[2] = self.base_matrix * Vec(0, 0, 1) * 40
        self.matrix = Matrix(self.base[0], self.base[1], self.base[2]).transpose()
        self.screen_size = screen_size

        self.light_direction = Vec(1, 1, 1).normalize()
        self.light_color = Vec(1, 1, 0.9)

        self.lights = []

    def change_base(self, matrix):
        self.base_matrix = matrix
        self.base[0] = self.base_matrix * Vec(1, 0, 0) * 40
        self.base[1] = self.base_matrix * Vec(0, 1, 0) * 40
        self.base[2] = self.base_matrix * Vec(0, 0, 1) * 40
        self.matrix = Matrix(self.base[0], self.base[1], ZERO3).transpose()
    def set_light_direction(self, v: Vec):
        assert v.dim() == 3
        self.light_direction = v.normalize()

    def set_light_color(self, col):
        assert col.dim() == 3
        self.light_color = col

    def add_point_light(self, pos, color=Vec(1, 1, 1)):
        self.lights.append(PointLight(pos, color))

    def to_screen(self, v):
        return (self.matrix * v)["xy"] + self.screen_size / 2

    def cam_dist(self, pos):
        return (self.matrix * pos).z



    def color(self, pos, normal, color):
        return self._intensity(pos, normal) * color

    def _intensity(self, pos, normal):
        res = self._radiance(normal) + self._lights(pos, normal)
        return Vec(max(min(res.r, 1), 0), max(0, min(res.g, 1)), max(0, min(res.b, 1)))

    def _radiance(self, normal):
        """ Met la lumière type Soleil
        Attention, elle suppose que regarder une face d'un côté, ou de l'autre ne change rien.
        """
        return abs(dot(normal, self.light_direction)) * self.light_color

    def _lights(self, pos: Vec, normal: Vec):
        normal = normal.normalize()
        if dot(self.base[2], normal) > 0: normal = -normal
        res = Vec(0, 0, 0)
        for light in self.lights:
            res += light.apply(pos, normal)
        return Vec(min(1, res.r), min(1, res.g), min(1, res.b))


if __name__ == "__main__":
    engine = ViewEngine(Vec(1100, 700))
    print(engine.base)
    print(engine.to_screen(Vec(2, 2, 2)))
