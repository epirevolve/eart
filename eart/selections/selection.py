# -*- coding: utf-8 -*-

import numpy as np
from ..background import BackFunction


class Selection(BackFunction):
    def __init__(self, *,
                 random_group=False, selection_shuffle=False):
        super(Selection, self).__init__()
        self._random_group = random_group
        self._selection_shuffle = selection_shuffle

    @staticmethod
    def _split_data(weights, data):
        c_weights = [len(data) * x for x in weights]
        slices = [int(sum(c_weights[:i])) for i in range(1, len(c_weights))]
        return np.split(data, slices)
    
    def _run(self, population):
        if not self._methods:
            raise ValueError('selection is not assigned')
        if not self._compiled:
            raise ValueError('compile is required before run')
        survivors = []
        remains = population[:]
        methods, weights = zip(*self._methods.values())
        if self._random_group:
            np.random.shuffle(remains)
        for method, data in zip(methods, self._split_data(weights, remains)):
            survivors.extend(method.run(data))
        if self._selection_shuffle:
            np.random.shuffle(survivors)
        return survivors
    
    def run(self, population):
        raise NotImplementedError()


class MarriageSelection(Selection):
    def run(self, population):
        survivors = self._run(population)
        while len(survivors) >= 2:
            yield survivors.pop(0), survivors.pop(0)


class TransitionSelection(Selection):
    def __init__(self, *, const_population_size=None,
                 random_group=False, selection_shuffle=False):
        super(TransitionSelection, self).__init__(random_group=random_group,
                                                  selection_shuffle=selection_shuffle)
        self._const_population_size = const_population_size
    
    def run(self, population):
        survivors = self._run(population)
        if self._const_population_size:
            remains = population[:]
            while len(survivors) < self._const_population_size:
                remains = list(set(remains) - set(survivors))
                survivors.extend(self._run(remains))
            survivors = survivors[:self._const_population_size]
        return survivors
