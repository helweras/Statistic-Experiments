from datetime import datetime, date
import random
import calendar
from .Child import Child


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

    def __init__(self, population: tuple, weight_born: tuple, second_name=None):
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
        self.second_name = second_name

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
        self.children = tuple(Child(self.gen_random_data(),
                                    second_name=self.second_name
                                    ) for _ in range(children_count))

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
