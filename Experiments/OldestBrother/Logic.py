from datetime import datetime, date
import random
import calendar
from math import sqrt
from random import shuffle


class Family:
    def __init__(self, population: tuple, weight_born):
        self.population = population
        self.children: tuple = ()
        self.weight = weight_born
        self.incubator()
        self.condition_child()
        self.children_count = 0

    def incubator(self):
        start, stop = self.population
        values = range(start, stop + 1)
        self.weight = self.weight[start - 1:]
        children_count = random.choices(values, weights=self.weight, k=1)[0]
        self.children_count = children_count
        self.children = tuple(Child(self.gen_random_data()) for _ in range(children_count))

    @staticmethod
    def gen_random_data():
        stop = datetime.now().year
        start = stop - 30

        year = random.randrange(start, stop)
        month = random.randrange(1, 13)
        count_day = calendar.monthrange(year, month)[1]
        day = random.randrange(1, count_day + 1)

        return date(year=year, month=month, day=day)

    def condition_child(self):
        len_children = len(self.children)
        for i in range(len_children - 1):
            for j in range(i + 1, len_children):
                child_1, child_2 = self.children[i], self.children[j]
                child_1.get_relative(child_2)
                child_2.get_relative(child_1)
                sex = {"Men": "brother", "Woman": "sister"}
                relative_sex_1 = sex[child_1.sex]
                relative_sex_2 = sex[child_2.sex]
                delta = (child_1.born_data - child_2.born_data).days
                if delta > 0:
                    child_1.older[relative_sex_2] += 1
                    child_2.younger[relative_sex_1] += 1
                elif delta < 0:
                    child_1.younger[relative_sex_2] += 1
                    child_2.older[relative_sex_1] += 1
                child_1.relative = True
                child_2.relative = True


class Child:
    def __init__(self, born_data):
        self.born_data = born_data
        self.sex = random.choice(("Men", "Woman"))
        self.older = {"brother": 0, "sister": 0}
        self.younger = {"brother": 0, "sister": 0}
        self.relative = False
        self.name = 0
        self.relative_list = []

    def get_num(self, num):
        self.name = num

    def get_relative(self, relative):
        if relative not in self.relative_list:
            self.relative_list.append(relative)


def gen_family(population: tuple, count_family=100, weight_born=(55, 33, 9, 2, 1)):
    list_family = tuple(Family(population, weight_born=weight_born) for _ in range(count_family))
    return list_family


def detected_relative(children_list: tuple[Child, ...]):
    children = random.choice(children_list)
    return children.relative


def all_children(family_list: tuple[Family, ...]) -> tuple:
    c = 1
    children_full_list = []
    for family in family_list:
        for child in family.children:
            child.get_num(c)
            c += 1

        children_full_list.extend(family.children)
    return tuple(children_full_list)


def exp_new_family():
    count = 0
    for i in range(100):
        family_list = gen_family((1, 5))
        children = all_children(family_list)
        count += detected_relative(children)

    return count / 100 * 100


def exp_old_family():
    family_list = gen_family((1, 5))
    children = all_children(family_list)
    # count = 0
    # for i in range(100):
    #     count += detected_relative(children)
    # return count / 100 * 100


def ret_children(r=False):
    f_list = gen_family((1, 5))
    if r:
        children = list(all_children(f_list))
        random.shuffle(children)
        return tuple(children)
    return all_children(f_list)


# Сделать расчеты формулой


# x = gen_family((1, 5), 1)
# x[0].condition_child()
# for ch in x[0].children:
#     print(ch.born_data)
#     print(ch.relative)
#     print(ch.sex)
#     print(ch.older)
#     print(ch.younger)
#     print("-----------")

# print(f"New = {exp_new_family()}")
# print(f"Old = {exp_old_family()}")
