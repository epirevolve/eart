# -*- coding: utf-8 -*-

import numpy as np
from ..background import BackFunction


class Crossover(BackFunction):
    def run(self, gene1, gene2):
        if not self._methods:
            raise ValueError('selection is not assigned')
        if not self.is_compiled:
            raise ValueError('compile is required before run')
        methods, weights = zip(*self._methods.values())
        method = np.random.choice(methods, p=weights)
        return method.run(gene1, gene2)
