import numpy as np


def get_forces(x, m):
    G = -9.79845085224335

    n, _ = x.shape

    d = np.zeros((n * (n - 1) // 2, 2))
    k = 0
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            d[k] = G * (x[i] - x[j]) / np.linalg.norm(x[i] - x[j]) ** 3
            k = k + 1
    d_idx = lambda i, j: j - (i ** 2 + 3 * i) // 2 + i * n - 1

    f = np.zeros((n, 2))
    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                sign = +1. if i < j else -1.
                f[i] += sign * m[j] * d[d_idx(i, j) if i < j else d_idx(j, i)]

    return f


def integrate(x, v, m, dt):
    w0 = -1.7024143839193153
    w1 = 1.3512071919596578
    c1 = w1 / 2.
    c4 = w1 / 2.
    c2 = (w0 + w1) / 2.
    c3 = (w0 + w1) / 2.
    d1 = w1
    d3 = w1
    d2 = w0

    x1 = x + c1 * v * dt
    a1 = get_forces(x=x1, m=m)
    v1 = v + d1 * a1 * dt

    x2 = x1 + c2 * v1 * dt
    a2 = get_forces(x=x2, m=m)
    v2 = v1 + d2 * a2 * dt

    x3 = x2 + c3 * v2 * dt
    a3 = get_forces(x=x3, m=m)
    v3 = v2 + d3 * a3 * dt

    x4 = x3 + c4 * v3 * dt
    v4 = v3

    return x4, v4
