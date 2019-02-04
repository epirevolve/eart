# -*- coding: utf-8 -*-

import numpy as np


class TournamentSelection:
    def __init__(self, *,
                 group_size=None, require_size=None):
        if not group_size and not require_size:
            raise ValueError('either group size or require size is needed')
        self._group_size = group_size
        self._require_size = require_size
        if not self._require_size:
            self._require_size = int(population_size / self._group_size)
        if not self._group_size:
            self._group_size = int(population_size / self._require_size)
    
    def run(self, population):
        group = np.random.choice(population, (self._require_size, self._group_size), replace=False)
        return [max(g, key=lambda f: f.adaptability) for g in group]
