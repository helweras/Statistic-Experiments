from Experiments.PlaygroundParadox.Components.ChildHouse import ChildHouse
import random


def gen_random_weight():
    points = sorted([random.randrange(101) for _ in range(4)])
    points = [0] + points + [100]

    weights = tuple(next_val - current for current, next_val in zip(points, points[1:]))

    return weights


def family_connect(child_list: list):
    check = [child_list[0].second_name]
    for child in child_list[1:]:
        if child.second_name in check:
            return True
        else:
            check.append(child.second_name)
    return False


def get_class(all_ch, value):
    result = random.sample(all_ch, value)
    for i in result:
        print(i.second_name, end=" ")
    print()
    return result


def blood_tiles(count_sim, value):
    c = 0
    weight = gen_random_weight()
    child_house = ChildHouse(weights_born=(55, 33, 9, 3, 1))
    all_children = child_house.all_children_list
    for _ in range(count_sim):
        result = random.sample(all_children, value)
        if family_connect(result):
            c += 1
        print(f"\r{c}", end="")
    print()
    return round(c / count_sim, 2) * 100


x = blood_tiles(100000, 20)
print(x)