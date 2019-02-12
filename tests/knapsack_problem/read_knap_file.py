# -*- coding: utf-8 -*-


def read_text(file):
    def _separate(s):
        _s = s.split()
        return float(_s[0]), int(_s[1])
    with open(file, 'r') as f:
        data = f.readlines()
    max_weight = data.pop(0)
    return float(max_weight), [_separate(x) for x in data]
