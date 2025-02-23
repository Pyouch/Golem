from Matrix import *
from Vec import *


class ViewEngine:
    base_matrix = Matrix.rotation_z(-3 * pi / 4) * Matrix.rotation_x(pi / 4)

    def __init__(self, screen_size):
        self.base = [0, 0, 0]
        self.base[0] = self.base_matrix * Vec(1, 0, 0) * 40
        self.base[1] = self.base_matrix * Vec(0, 1, 0) * 40
        self.base[2] = self.base_matrix * Vec(0, 0, 1) * 40
        self.matrix = Matrix(self.base[0], self.base[1], ZERO3).transpose()
        self.screen_size = screen_size

        self.light_direction = Vec(1, 1, 1).normalize()
        self.light_color = Vec(1, 1, 0.9)

    def set_light_direction(self, v: Vec):
        assert v.dim() == 3
        self.light_direction = v.normalize()

    def set_light_color(self, col):
        assert col.dim() == 3
        self.light_color = col

    def to_screen(self, v):
        return (self.matrix * v)["xy"] + self.screen_size / 2

    def color(self, v, normal, color):
        return self._radiance(normal, color)

    def _radiance(self, normal, color):
        """ Met la lumière type Soleil
        Attention, elle suppose que regarder une face d'un côté, ou de l'autre ne change rien.
        """
        return abs(dot(normal, self.light_direction)) * self.light_color * color


if __name__ == "__main__":
    engine = ViewEngine(Vec(1100, 700))
    print(engine.base)
    print(engine.to_screen(Vec(2, 2, 2)))
