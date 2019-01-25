# -*- coding: utf-8 -*-

import numpy as np


def tournament_selection(*args):
    population, require_count, *_ = args
    group_size = int(len(population) / require_count)
    group = np.random.choice(population, (require_count, group_size), replace=False)
    return [max(g, key=lambda f: f.adaptability) for g in group]
