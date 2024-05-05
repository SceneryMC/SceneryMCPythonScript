A = 52969


def operation_naive_impl(A, B, C):
    while A != 1:
        while True:
            B += 1
            C += 1
            if A % (B + 1) == 0:
                A = A // (B + 1) * (B ** C)
                B = 0
                break
    return C


print(operation_naive_impl(A, 0, 0))
