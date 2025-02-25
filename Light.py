from Vec import *


class PointLight:
    def __init__(self, pos: Vec, color: Vec):
        self.pos = pos
        self.color = color

    def apply(self, v, normal: Vec):
        """ We suppose that normal is normalized """
        d = self.pos - v
        return self.color * dot(normal, d) / max(d.size(), 1)

