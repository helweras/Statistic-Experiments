import random


def gen_random_weight():
    points = sorted([random.randrange(101) for _ in range(4)])
    points = [0] + points + [100]

    weights = tuple(next_val - current for current, next_val in zip(points, points[1:]))

    return weights
