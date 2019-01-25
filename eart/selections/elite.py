# -*- coding: utf-8 -*-

elite_rate = 0.05


def elite_selection(*args):
    population, *_ = args
    return population[: int(elite_rate * len(population))]
