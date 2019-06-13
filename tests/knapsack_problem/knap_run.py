# -*- coding: utf-8 -*-

import argparse
import time

from eart import Genetic
from eart import ParentSelection
from eart import SurvivorSelection
from eart import Mutation
from eart import Crossover
from eart.selections import EliteSelection
from eart.selections import TournamentSelection
from eart.mutations import InvertMutation
from eart.mutations import TranslocateMutation
from eart.mutations import WholeMutation
from eart.crossovers import SinglePointCrossover
from eart.crossovers import MultiPointCrossover
from eart.crossovers import UniformityCrossover
from eart.crossovers import TwoPointCrossover
from eart.crossovers import MirrorCrossover

from tests.knapsack_problem import read_knap_file as rtf


class Evaluation:
    def __init__(self, n_max_, factors_):
        self._n_max = n_max_
        self._factors = factors_
    
    def evaluate(self, gene):
        packed = [x for x, y in zip(self._factors, gene) if y == 1]
        weights, valus = zip(*packed)
        if sum(weights) > self._n_max:
            return 0
        return sum(valus)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    param_args = parser.parse_args()
    
    print('start knapsack problem')
    
    n_max, factors = rtf.read_text(param_args.file)

    evaluation = Evaluation(n_max, factors).evaluate
    
    genetic = Genetic(evaluation=evaluation, base_kind=[0, 1], gene_size=len(factors),
                      homo_progeny_restriction=True)
    parent_selection = ParentSelection(selection_shuffle=True)
    parent_selection.add(EliteSelection(), 0.05)
    parent_selection.add(TournamentSelection(group_size=2))
    genetic.parent_selection = parent_selection
    survivor_selection = SurvivorSelection(const_population_size=genetic.population_size)
    survivor_selection.add(EliteSelection(), 0.05)
    survivor_selection.add(TournamentSelection(group_size=3))
    genetic.survivor_selection = survivor_selection
    mutation = Mutation(proliferate_mutation=True)
    mutation.add(WholeMutation(), 0.05)
    mutation.add(InvertMutation(), 0.5)
    mutation.add(TranslocateMutation())
    genetic.mutation = mutation
    crossover = Crossover()
    crossover.add(SinglePointCrossover(), 0.1)
    crossover.add(MultiPointCrossover())
    crossover.add(UniformityCrossover())
    crossover.add(TwoPointCrossover())
    crossover.add(MirrorCrossover())
    genetic.crossover = crossover
    
    i = genetic.compile()
    print("era: {:>4}, adaptability: {}, elapsed time {}".format(genetic.era, i.adaptability, 0))

    s = time.clock()

    for i in genetic.run_by_step():
        print("era: {:>4}, adaptability: {}, elapsed time {}".format(genetic.era, i.adaptability, time.clock() - s))

    print("elapsed time:{}".format(time.clock() - s))
