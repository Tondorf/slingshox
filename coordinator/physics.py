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


def integrate(xs, vs, fs, ms, dt):
    assert len(xs) == len(vs) == len(ms)
    assert dt > 0.

    if fs is None:
        fs = get_forces(xs=xs, ms=ms)

    next_xs = [x + v * dt + a * dt ** 2 / 2. for x, v, a in zip(xs, vs, fs)]
    next_fs = get_forces(xs=next_xs, ms=ms)
    next_vs = [v + (a + next_a) * dt / 2. for v, a, next_a in zip(vs, fs, next_fs)]

    return next_xs, next_vs, next_fs, ms, dt
