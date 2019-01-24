# -*- coding: utf-8 -*-

import math
import time
import tkinter
import argparse
from eart.genetic import Genetic
from eart.selections import Tournament
from eart.mutations import Inverting
from eart.crossovers import Circuit
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
        t.adaptability = 1 / self._path_length(t.gene)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    param_args = parser.parse_args()

    point_table = rtf.read_text(param_args.file)
    root = tkinter.Tk()

    max_x = max([x[0] for x in point_table]) + 20
    max_y = max([x[1] for x in point_table]) + 20

    canvas = DisplayCanvas(root, max_x, max_y)
    evaluation = Evaluation(point_table).evaluate
    genetic = Genetic(len(point_table), evaluation,
                      Tournament(3), Inverting(), Circuit())
    genetic.make_protobiont()

    s = time.clock()

    for i in genetic():
        if genetic.era == 1:
            canvas.draw_point([point_table[i] for i in i.gene])
        canvas.draw_path([point_table[i] for i in i.gene])
        print("era: {:>4}, adaptability: {}".format(genetic.era, i.adaptability))

    print("elapsed time:{}".format(time.clock() - s))

    root.mainloop()
