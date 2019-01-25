# -*- coding: utf-8 -*-

from ..indivisual import Individual


def whole_mutation(individual):
    individual = Individual.protobiont(individual.born_at)
    return individual
