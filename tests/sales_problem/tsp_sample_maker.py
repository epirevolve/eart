# -*- coding: utf-8 -*-

import random

n_max = 300
cities = [(random.randint(0, 1500), random.randint(0, 750)) for _ in range(n_max)]

cities = set(cities)
points = ['{} {}'.format(*x) for x in cities]

with open('./samples/sample8.txt', 'w') as f:
    f.write('\n'.join(points))
