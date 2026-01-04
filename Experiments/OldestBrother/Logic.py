from datetime import datetime, date
import random
import calendar
from math import sqrt
from random import shuffle


class Family:
    """
    Класс, представляющий семью и генерирующий детей с заданными параметрами.

    Attributes
    ----------
    population : tuple[int, int]
        Диапазон возможного количества детей в семье (min, max).
    children : tuple[Child, ...]
        Кортеж объектов Child, представляющих детей в семье.
    weight : list[int]
        Список весов для вероятностного выбора количества детей.
    children_count : int
        Фактическое количество детей в семье после генерации.
    """

    def __init__(self, population: tuple, weight_born: tuple):
        """
        Инициализация семьи. Генерация детей происходит сразу.

        Parameters
        ----------
        population : tuple[int, int]
            Диапазон количества детей (min, max) для генерации.
        weight_born : list[int]
            Список весов для генерации количества детей.
        """
        self.population = population
        self.children: tuple = ()
        self.weight = weight_born
        self.children_count = 0

        # Генерация детей и присвоение условий
        self.incubator()
        self.condition_child()

    def incubator(self):
        """
        Генерация количества детей в семье и их данных.

        Использует random.choices для вероятностного выбора числа детей.
        После определения количества детей создаются объекты Child.
        """
        start, stop = self.population
        values = range(start, stop + 1)
        self.weight = self.weight[start - 1:]  # корректировка весов под диапазон
        children_count = random.choices(values, weights=self.weight, k=1)[0]
        self.children_count = children_count

        # Создание кортежа объектов Child
        self.children = tuple(Child(self.gen_random_data()) for _ in range(children_count))

    @staticmethod
    def gen_random_data() -> date:
        """
        Генерация случайной даты рождения для ребенка.

        Возраст детей ограничен 30 годами.

        Returns
        -------
        datetime.date
            Дата рождения ребенка.
        """
        stop = datetime.now().year
        start = stop - 30

        year = random.randrange(start, stop)
        month = random.randrange(1, 13)
        count_day = calendar.monthrange(year, month)[1]
        day = random.randrange(1, count_day + 1)

        return date(year=year, month=month, day=day)

    def condition_child(self):
        """
        Определение отношений между детьми в семье: старше/младше и брат/сестра.

        Для каждой пары детей вычисляется разница по дате рождения и обновляются
        соответствующие счетчики older и younger.
        """
        len_children = len(self.children)
        for i in range(len_children - 1):
            for j in range(i + 1, len_children):
                child_1, child_2 = self.children[i], self.children[j]

                # Добавляем друг друга в список родственников
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

                # Флаг наличия родственников
                child_1.relative = True
                child_2.relative = True


class Child:
    """
    Класс, представляющий одного ребенка.

    Attributes
    ----------
    born_data : datetime.date
        Дата рождения ребенка.
    sex : str
        Пол ребенка ('Men' или 'Woman').
    older : dict[str, int]
        Счетчики старших братьев и сестер.
    younger : dict[str, int]
        Счетчики младших братьев и сестер.
    relative : bool
        Флаг наличия родственников в семье.
    name : int
        Порядковый номер ребенка.
    relative_list : list[Child]
        Список других детей в семье.
    """

    def __init__(self, born_data: date):
        self.born_data = born_data
        self.sex = random.choice(("Men", "Woman"))
        self.older = {"brother": 0, "sister": 0}
        self.younger = {"brother": 0, "sister": 0}
        self.relative = False
        self.name = 0
        self.relative_list = []

    def get_num(self, num: int):
        """
        Присвоение порядкового номера ребенку.
        """
        self.name = num

    def get_relative(self, relative):
        """
        Добавление ребенка в список родственников, если его там еще нет.

        Parameters
        ----------
        relative : Child
            Другой ребенок в семье.
        """
        if relative not in self.relative_list:
            self.relative_list.append(relative)


class ChildHouse:
    """
    Класс для работы с набором семей и всех детей.

    Реализует методы для анализа вероятности быть единственным ребенком,
    иметь братьев или сестер, перемешивания детей и получения статистики.
    """

    def __init__(self, population: tuple = (1, 5)):
        """
        Инициализация ChildHouse и генерация семей и детей.

        Parameters
        ----------
        population : tuple[int, int], optional
            Диапазон количества детей в семьях (min, max), по умолчанию (1, 5).
        """
        self.family_list = self.gen_family(population)
        self.all_children_list = self.all_children()
        self.chance_singleton_child()
        self.chance_sibling_child()

    @staticmethod
    def gen_family(population: tuple, count_family=100, weight_born=(55, 33, 9, 2, 1)) -> tuple[Family, ...]:
        """
        Генерация заданного количества семей.

        Parameters
        ----------
        population : tuple[int, int]
            Диапазон количества детей в семье.
        count_family : int, optional
            Количество семей для генерации, по умолчанию 100.
        weight_born : tuple[int], optional
            Вероятности для генерации количества детей, по умолчанию (55,33,9,2,1).

        Returns
        -------
        tuple[Family, ...]
            Кортеж объектов Family.
        """
        list_family = tuple(Family(population, weight_born=weight_born) for _ in range(count_family))
        return list_family

    def get_shuffle_children(self, r=True) -> tuple:
        """
        Получение всех детей в перемешанном порядке или по умолчанию.

        Parameters
        ----------
        r : bool, optional
            Если True — возвращает перемешанный кортеж детей, иначе оригинальный список.

        Returns
        -------
        tuple
            Кортеж объектов Child.
        """
        if r:
            children = list(self.all_children_list)
            random.shuffle(children)
            return tuple(children)
        return self.all_children_list

    def get_value_family(self) -> tuple:
        """
        Подсчет количества семей по числу детей.

        Returns
        -------
        tuple
            Отсортированный кортеж (число детей, количество семей).
        """
        value = {}
        for family in self.family_list:
            value[family.children_count] = value.get(family.children_count, 0) + 1
        return tuple(sorted(tuple(value.items()), key=lambda x: x[0]))

    def get_family_list(self) -> tuple:
        """
        Получение списка всех семей.

        Returns
        -------
        tuple[Family, ...]
            Кортеж объектов Family.
        """
        return self.family_list

    def all_children(self) -> tuple:
        """
        Формирование списка всех детей из всех семей с присвоением номера.

        Returns
        -------
        tuple[Child, ...]
            Кортеж объектов Child.
        """
        c = 1
        children_full_list = []
        for family in self.family_list:
            for child in family.children:
                child.get_num(c)
                c += 1
            children_full_list.extend(family.children)
        return tuple(children_full_list)

    def detected_relative(self) -> bool:
        """
        Случайным образом проверяет наличие родственников у ребенка.

        Returns
        -------
        bool
            True, если у ребенка есть родственники, иначе False.
        """
        children = random.choice(self.all_children_list)
        return children.relative

    def chance_singleton_child(self) -> float:
        """
        Вероятность, что ребенок единственный в семье.

        Returns
        -------
        float
            Процент детей-одиночек.
        """
        single_family = self.get_value_family()[0][-1]
        return round(single_family / len(self.all_children_list) * 100, 2)

    def chance_sibling_child(self) -> float:
        """
        Вероятность, что ребенок имеет хотя бы одного брата или сестру.

        Returns
        -------
        float
            Процент детей с братьями или сестрами.
        """
        large_family = len(self.all_children_list) - self.get_value_family()[0][-1]
        return round(large_family / len(self.all_children_list) * 100, 2)

# def ret_children(family_list: tuple[Family, ...] = f_list, r=True):
#     if r:
#         children = list(all_children(family_list))
#         random.shuffle(children)
#         return tuple(children)
#     return all_children(f_list)
#
#
# def get_value_family(family_list: tuple[Family, ...] = f_list):
#     value = {}
#     for family in family_list:
#         value[family.children_count] = value.get(family.children_count, 0) + 1
#     return sorted(tuple(value.items()), key=lambda x: x[0])

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

# def detected_relative(children_list: tuple[Child, ...]):
#     children = random.choice(children_list)
#     return children.relative
#
#
# def all_children(family_list: tuple[Family, ...]) -> tuple:
#     c = 1
#     children_full_list = []
#     for family in family_list:
#         for child in family.children:
#             child.get_num(c)
#             c += 1
#
#         children_full_list.extend(family.children)
#     return tuple(children_full_list)
