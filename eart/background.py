# -*- coding: utf-8 -*-


class BackFunction:
    def __init__(self):
        self._methods = {}
        self.is_compiled = False
    
    def add(self, method, weight=None):
        self._methods[type(method)] = (method, weight)
        self.is_compiled = False

    def compile(self):
        methods, weights = zip(*self._methods.values())
        if sum([x or 0 for x in weights]) > 1:
            raise ValueError('sum of weight must be less than 1')
        none_count = weights.count(None)
        if none_count:
            r_weight = (1 - sum([x or 0 for x in weights])) / none_count
            self._methods = {x: (y[0], y[1] or r_weight) for x, y in self._methods.items()}
            weights = [x or r_weight for x in weights]
        if sum(weights) != 1:
            raise ValueError('sum of weight must be 1')
        self.is_compiled = True
