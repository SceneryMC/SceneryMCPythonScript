from math import *
from scipy import integrate

n = 365
epsilon = 23.5 * pi / 180
N = 1000


def acos_extended(x):
    if -1 <= x <= 1:
        return acos(x)
    else:
        return float(x < -1) * pi


def I_without_atmosphere(k, a):
    r_k = asin(sin(2 * pi * k / n) * sin(epsilon))
    b_k = acos_extended(-tan(r_k) * tan(a))
    return sin(r_k) * sin(a) * b_k + cos(r_k) * cos(a) * sin(b_k)


def I_D_ratio(x):
    AM = 1 / (sin(x) + 0.50572 * (6.07995 + x * 180 / pi) ** -1.6364)
    return 1.353 * (0.7 ** (AM ** 0.678)) if round(x, 10) != round(pi / 2, 10) else 0


def I_with_atmosphere(k, a):
    r_k = asin(sin(2 * pi * k / n) * sin(epsilon))
    b_k = acos_extended(-tan(r_k) * tan(a))
    eta = lambda x: sin(r_k) * sin(a) - cos(r_k) * cos(a) * cos(x)
    ans = integrate.quad(lambda x: eta(x) * I_D_ratio(asin(eta(x))), pi - b_k, pi + b_k)[0] if b_k else 0
    return ans


for a in range(0, 90 + 1):
    s1 = s2 = 0
    for k in range(n):
        s1 += I_without_atmosphere(k, a * pi / 180)
        s2 += I_with_atmosphere(k, a * pi / 180)
    s1 = s1 / n / pi
    s2 = s2 / n / (2 * pi)
    print(f"{s2}")
