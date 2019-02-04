# -*- coding: utf-8 -*-

import numpy as np


class Selection:
    def __init__(self, *,
                 parent_shuffle=False, marriage_shuffle=False):
        self._parent_shuffle = parent_shuffle
        self._marriage_shuffle = marriage_shuffle
        
        self._methods = {}
    
    def add(self, method, weight=None):
        self._methods[type(method)] = (method, weight)

    @staticmethod
    def _split_data(weights, data):
        if sum([x or 0 for x in weights]) > 1:
            raise ValueError('sum of weight must be less than 1')
        none_count = weights.count(None)
        if none_count:
            r_weight = 1 - sum([x or 0 for x in weights]) / none_count
            weights = [x or r_weight for x in weights]
        if sum(weights) != 1:
            raise ValueError('sum of weight must be 1')
        c_weights = [len(data) * x for x in weights]
        slices = [int(sum(c_weights[:i])) for i in range(1, len(c_weights))]
        return np.split(data, slices)
    
    def _run(self, population):
        if not self._methods:
            raise ValueError('selection is not assigned')
        survivors = []
        remains = population[:]
        methods, weights = zip(*self._methods.values())
        if self._parent_shuffle:
            np.random.shuffle(remains)
        for method, data in zip(methods, self._split_data(weights, remains)):
            survivors.extend(method.run(data))
        if self._marriage_shuffle:
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
    def __init__(self, *, population_size,
                 parent_shuffle=False, marriage_shuffle=False):
        super(TransitionSelection, self).__init__(parent_shuffle=parent_shuffle,
                                                  marriage_shuffle=marriage_shuffle)
        self._population_size = population_size
    
    def run(self, population):
        survivors = self._run(population)
        return survivors
