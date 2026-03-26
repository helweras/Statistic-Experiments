import random
from .Family import Family


class ChildHouse:
    """
    Класс для работы с набором семей и всех детей.

    Реализует методы для анализа вероятности быть единственным ребенком,
    иметь братьев или сестер, перемешивания детей и получения статистики.
    """

    def __init__(self, weights_born, count_family=100, population: tuple = (1, 5)):
        """
        Инициализация ChildHouse и генерация семей и детей.

        Parameters
        ----------
        population : tuple[int, int], optional
            Диапазон количества детей в семьях (min, max), по умолчанию (1, 5).
        """
        self.family_list = self.gen_family(population, weight_born=weights_born, count_family=count_family)
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

    def get_child_distribution(self):
        child_distribution = {"Дети без братьев и сестер": self.chance_singleton_child(),
                              "Дети c братьями и сестрами": self.chance_sibling_child()}
        return child_distribution
