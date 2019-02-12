# -*- coding: utf-8 -*-

import math
import time
import tkinter
import argparse

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
from eart.crossovers import OrderlyCrossover
from eart.crossovers import CircuitCrossover

from tests.sales_problem import read_tsp_file as rtf
from tests.sales_problem.draw_canvas import DisplayCanvas


class Evaluation:
    def __init__(self, _table):
        self._distance_table = []
        self._map_distance(_table)

    def _map_distance(self, _table):
        self._gene_size = len(_table)
        self._distance_table = [[0] * self._gene_size for _ in range(self._gene_size)]
        for t in range(self._gene_size):
            for j in range(self._gene_size):
                if t != j:
                    dx = _table[t][0] - _table[j][0]
                    dy = _table[t][1] - _table[j][1]
                    self._distance_table[t][j] = math.hypot(dx, dy)

    def _path_length(self, path):
        n = 0
        for t in range(1, len(path)):
            n += self._distance_table[path[t - 1]][path[t]]
        n += self._distance_table[path[0]][path[-1]]
        return n

    def evaluate(self, gene):
        return 1 / self._path_length(gene)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    param_args = parser.parse_args()

    print('start sales problem')

    point_table = rtf.read_text(param_args.file)
    print('{} points are inputted as city'.format(len(point_table)))

    root = tkinter.Tk()

    max_x = max([x[0] for x in point_table]) + 20
    max_y = max([x[1] for x in point_table]) + 20

    canvas = DisplayCanvas(root, max_x, max_y)
    evaluation = Evaluation(point_table).evaluate
    
    genetic = Genetic(evaluation=evaluation,
                      base_kind=range(len(point_table)), homo_progeny_restriction=True)
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
    crossover.add(OrderlyCrossover())
    crossover.add(CircuitCrossover())
    genetic.crossover = crossover
    
    i = genetic.compile()
    canvas.draw_point([point_table[i] for i in i.gene])
    canvas.draw_path([point_table[i] for i in i.gene])
    print("era: {:>4}, adaptability: {}, elapsed time {}".format(genetic.era, i.adaptability, 0))
    
    s = time.clock()
    
    for i in genetic.run_by_step():
        canvas.draw_path([point_table[i] for i in i.gene])
        print("era: {:>4}, adaptability: {}, elapsed time {}".format(genetic.era, i.adaptability, time.clock() - s))
    
    print("elapsed time:{}".format(time.clock() - s))

    root.mainloop()
