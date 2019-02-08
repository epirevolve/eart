# -*- coding: utf-8 -*-

import math
import time
import tkinter
import argparse
from eart import (
    Genetic, MarriageSelection, TransitionSelection,
    Mutation, Crossover
)
from eart.selections import (
    EliteSelection, TournamentSelection
)
from eart.mutations import (
    InvertMutation, TranslocateMutation, WholeMutation
)
from eart.crossovers import (
    OrderlyCrossover, CircuitCrossover
)
from tests.sales_problem.utility import read_tsp_file as rtf
from tests.sales_problem.utility.draw_canvas import DisplayCanvas


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

    def evaluate(self, t):
        return 1 / self._path_length(t)


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
    marriage_selection = MarriageSelection(selection_shuffle=True)
    marriage_selection.add(EliteSelection(), 0.05)
    marriage_selection.add(TournamentSelection(group_size=2))
    marriage_selection.compile()
    genetic.marriage_selection = marriage_selection
    transition_selection = TransitionSelection(const_population_size=genetic.population_size)
    transition_selection.add(EliteSelection(), 0.05)
    transition_selection.add(TournamentSelection(group_size=3))
    transition_selection.compile()
    genetic.transition_selection = transition_selection
    mutation = Mutation(proliferate_mutation=True)
    mutation.add(WholeMutation(), 0.05)
    mutation.add(InvertMutation(), 0.5)
    mutation.add(TranslocateMutation())
    mutation.compile()
    genetic.mutation = mutation
    crossover = Crossover()
    crossover.add(OrderlyCrossover())
    crossover.add(CircuitCrossover())
    crossover.compile()
    genetic.crossover = crossover
    
    i = genetic.init()
    canvas.draw_point([point_table[i] for i in i.gene])
    canvas.draw_path([point_table[i] for i in i.gene])
    print("era: {:>4}, adaptability: {}, elapsed time {}".format(genetic.era, i.adaptability, 0))
    
    s = time.clock()
    
    for i in genetic.run_by_step():
        canvas.draw_path([point_table[i] for i in i.gene])
        print("era: {:>4}, adaptability: {}, elapsed time {}".format(genetic.era, i.adaptability, time.clock() - s))
    
    print("elapsed time:{}".format(time.clock() - s))

    root.mainloop()
