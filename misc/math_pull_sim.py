import random


def pull_once(n, p):
    hit = 0
    for _ in range(n):
        hit += (random.random() < 0.5)
    if extra := (hit / n > 0.5 and random.random() < p):
        hit += (random.random() < 0.5)
    return hit, extra


T = 10000
n = 4
p = 0.5
total_hit = 0
total_extra = 0
for _ in range(T):
    hit, extra = pull_once(n, p)
    total_hit += hit
    total_extra += extra
print(total_hit / (T * n + total_extra))