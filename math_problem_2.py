import itertools as it
import random as r

r.seed(0)
n = 5
xi = 3
delta = []
for i in range(xi-1):
    delta.append([r.uniform(0, 1 / xi) for j in range(n)])
    delta[i].insert(0, 0)
last_prob = [0]
for j in range(1, n+1):
    last = 1
    for i in range(xi-1):
        last -= delta[i][j]
    last_prob.append(last)
delta.append(last_prob)
print(delta)

prob_enum = {}
for p in it.product(range(xi), repeat=n-1):
    prob = 1
    for j in range(n-1):
        prob *= delta[p[j]][j+1]
    serial = tuple(p.count(j) for j in range(xi))
    prob_enum[serial] = prob_enum.get(serial, 0) + prob
print(prob_enum)
print(sum(list(x for x in prob_enum.values())))

prob_dp = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]
prob_dp[1][1][0], prob_dp[1][0][1], prob_dp[1][0][0] = delta[0][1], delta[1][1], delta[2][1]
for i in range(2, n):
    for l1 in range(0, i+1):
        for l2 in range(0, i+1-l1):
            tmp = 0
            if l1 >= 1:
                tmp += prob_dp[i-1][l1-1][l2] * delta[0][i]
            if l2 >= 1:
                tmp += prob_dp[i-1][l1][l2-1] * delta[1][i]
            if i-1 >= l1+l2:
                tmp += prob_dp[i-1][l1][l2] * delta[2][i]
            prob_dp[i][l1][l2] = tmp
ls_sum = []
for x in range(n-1, -1, -1):
    for y in range(n-1-x, -1, -1):
        print((n-1, x, y), prob_dp[n-1][x][y])
        ls_sum.append(prob_dp[n-1][x][y])
print(sum(ls_sum))

