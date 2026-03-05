from datetime import datetime, date
import random
import calendar


class Family:
    def __init__(self, population: tuple):
        self.population = population
        self.children: tuple = ()
        self.incubator()

    def incubator(self):
        start, stop = self.population
        children_count = random.randrange(start, stop + 1)
        self.children = tuple(Child(self.gen_random_data()) for i in range(children_count))

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
        for i in range(len_children-1):
            for j in range(i+1, len_children):
                child_1, child_2 = self.children[i], self.children[j]
                sex = {"Men":"brother", "Woman": "sister"}
                relative_sex_1 =sex[child_1.sex]
                relative_sex_2 =sex[child_2.sex]
                delta = (child_1.born_data - child_2.born_data).days
                if delta > 0:
                    child_1.older[relative_sex_2] += 1
                    child_2.younger[relative_sex_1] += 1
                elif delta < 0:
                    child_1.younger[relative_sex_2] += 1
                    child_2.older[relative_sex_1] += 1




class Child:
    def __init__(self, born_data):
        self.born_data = born_data
        self.sex = random.choice(("Men", "Woman"))
        self.older = {"brother":0 , "sister":0}
        self.younger = {"brother":0 , "sister":0}

def gen_family(population: tuple, count_family=100):
    list_family = tuple(Family(population) for i in range(count_family))
    return list_family

x = gen_family((4,6), 1)
x[0].condition_child()
for ch in x[0].children:
    print(ch.born_data)
    print(ch.sex)
    print(ch.older)
    print(ch.younger)
    print("-----------")



