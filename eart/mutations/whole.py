# -*- coding: utf-8 -*-

from ..indivisual import Individual


class Whole:
    def __call__(self, individual):
        return Individual(individual.id, len(individual.gene), individual.born_at)
