from Vec import *


class PointLight:
    def __init__(self, pos: Vec, color: Vec, power=1):
        self.pos = pos
        self.color = color
        self.power = power

    def apply(self, v, normal: Vec):
        """ We suppose that normal is normalized """
        d = (self.pos - v)
        length = d.size()
        d = d.normalize()
        return self.color * max(dot(normal, d), 0) / max(length/self.power, 1)

