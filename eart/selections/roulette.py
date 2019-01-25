# -*- coding: utf-8 -*-

import numpy as np


def roulette_selection(*args):
    population, demand_count = args
    s = sum([w.adaptability for w in population])
    return np.random.choice(population, demand_count, replace=False,
                            p=[w.adaptability / s for w in population])
