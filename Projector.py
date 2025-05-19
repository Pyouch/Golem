from Vec import *


class Projector:
    def __init__(self, mat):
        self.matrix = mat

    def project(self, vertices) -> list[Vec]:
        res = []
        for vert in vertices:
            res.append((self.matrix * vert.add_dim(1)).remove_dim(2))
        return res

    def set_matrix(self, mat):
        self.matrix = mat


