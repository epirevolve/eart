# -*- coding: utf-8 -*-

import numpy as np


class Roulette:
    def __init__(self):
        pass
    
    def __call__(self, *args, **kwargs):
        population, demand_count = args
        s = sum([w.adaptability for w in population])
        return np.random.choice(population, demand_count, replace=False, p=[w.adaptability / s for w in population])
