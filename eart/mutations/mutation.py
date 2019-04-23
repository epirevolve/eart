# -*- coding: utf-8 -*-

import numpy as np
from ..background import BackFunction


class Mutation(BackFunction):
    def __init__(self, *,
                 mutation_rate=0.01, proliferate_mutation=False,
                 proliferate_max=0.1, proliferate_rate=0.0001):
        super(Mutation, self).__init__()
        self._mutation_rate = mutation_rate
        self._proliferate_mutation = proliferate_mutation
        self._proliferate_max = proliferate_max
        self._proliferate_rate = proliferate_rate
    
    def proliferate(self):
        if not self._proliferate_mutation or self._mutation_rate > self._proliferate_max:
            return
        self._mutation_rate += self._proliferate_rate
    
    def _run(self, individual):
        if not self.is_compiled:
            raise ValueError('compile is required before run')
        methods, weights = zip(*self._methods.values())
        method = np.random.choice(methods, p=weights)
        method.run(individual)
    
    def run(self, individual):
        try:
            if np.random.rand() < self._mutation_rate:
                self._run(individual)
        except Exception as e:
            print("### error on mutation process.")
            print(e)
