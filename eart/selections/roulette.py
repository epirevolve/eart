# -*- coding: utf-8 -*-

import numpy as np


class RouletteSelection:
    def __init__(self, require_count):
        self._require_count = require_count
    
    def run(self, population):
        s = sum([w.adaptability for w in population])
        return np.random.choice(population, self._require_count, replace=False,
                                p=[w.adaptability / s for w in population])
