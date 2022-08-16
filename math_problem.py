from math import *


def f(x):
    if 1 >= x >= -1:
        return acos(x)
    elif x > 1:
        return 0
    else:
        return pi


n = 365
epi = 0.4089888
for i in range(0, 91, 1):
    total = 0
    a = i * pi / 180
    for k in range(n):
        rk = asin(sin(2 * pi * k / n) * sin(epi))
        bk = f(-tan(rk) * tan(a))
        total += (sin(rk) * sin(a) * bk + cos(rk) * cos(a) * sin(bk))
    total /= (pi * n)
    print(total)