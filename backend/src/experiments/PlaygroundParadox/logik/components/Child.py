from datetime import date
import random


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

    def __init__(self, born_data: date, second_name=None):
        self.born_data = born_data
        self.sex = random.choice(("Men", "Woman"))
        self.older = {"brother": 0, "sister": 0}
        self.younger = {"brother": 0, "sister": 0}
        self.relative = False
        self.name = 0
        self.relative_list = []
        self.second_name = second_name

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
