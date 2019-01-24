# -*- coding: utf-8 -*-

import numpy as np


class Tournament:
    def __init__(self, size):
        self._size = size
    
    def __call__(self, *args):
        population, *_ = args
        length = int(len(population) / self._size)
        group = np.random.choice(population, (length, self._size), replace=False)
        return [max(g, key=lambda f: f.adaptability) for g in group]
