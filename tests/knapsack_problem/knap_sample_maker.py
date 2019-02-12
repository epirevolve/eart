# -*- coding: utf-8 -*-

import random


n_max = 300
weight_values = [(round(random.uniform(0.1, 10), 1), random.randint(100, 2000)) for _ in range(n_max)]

factors = ['{} {}'.format(*x) for x in weight_values]

p = sum(map(lambda x: x[0], weight_values)) / 3

with open('./samples/sample1.txt', 'w') as f:
    f.write('{}\n'.format(round(random.uniform(p, p * 2), 2)))
    f.write('\n'.join(factors))
