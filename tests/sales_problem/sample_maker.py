# -*- coding: utf-8 -*-

import random

cities = []
n_max = 100

for n in range(n_max):
    cities.append((random.randint(0, 750), random.randint(0, 750)))

cities = set(cities)
points = []
for city in cities:
    points.append('{} {}'.format(*city))

with open('./samples/sample8.txt', 'w') as f:
    f.write('\n'.join(points))
