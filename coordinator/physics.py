import numpy as np


def get_forces(xs, ms):
    assert len(xs) == len(ms)
    G = 9.79845085224335

    fs = []
    for x in xs:
        f = 0.
        for u, m in zip(xs, ms):
            r = x - u
            norm = np.linalg.norm(r)
            if norm > 1e-10:
                f -= G * r * m / norm ** 3
        fs.append(f)

    return np.array(fs)


def integrate(xs, vs, ms, dt):
    assert len(xs) == len(vs)

    w0 = -1.7024143839193153
    w1 = 1.3512071919596578
    c1 = w1 / 2.
    c4 = w1 / 2.
    c2 = (w0 + w1) / 2.
    c3 = (w0 + w1) / 2.
    d1 = w1
    d3 = w1
    d2 = w0

    x1 = [x + c1 * v * dt for x, v in zip(xs, vs)]
    a1 = get_forces(xs=x1, ms=ms)
    v1 = [v + d1 * a * dt for v, a in zip(vs, a1)]

    x2 = [x + c2 * v * dt for x, v in zip(x1, v1)]
    a2 = get_forces(xs=x2, ms=ms)
    v2 = [v + d2 * a * dt for v, a in zip(v1, a2)]

    x3 = [x + c3 * v * dt for x, v in zip(x2, v2)]
    a3 = get_forces(xs=x3, ms=ms)
    v3 = [v + d3 * a * dt for v, a in zip(v2, a3)]

    x4 = [x + c4 * v * dt for x, v in zip(x3, v3)]
    v4 = v3

    return x4, v4
