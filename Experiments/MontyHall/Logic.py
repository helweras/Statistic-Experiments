import random


class Door:
    """Класс описывающий состояние двери"""

    def __init__(self, prize=False):
        self.prize = prize  # есть ли приз за дверью

    def get_prize(self):
        """Присваивает True self.prize"""
        self.prize = True


strategy = (True, False)  # Стратегии менять, не менять


def put_the_prize(door_list: list[Door], count_prize=1):
    """Случайным дверям в атрибут self.prize присваивается значение True
    Количество дверей определяется count_prize"""
    choice_doors = random.sample(door_list, count_prize)
    for door in choice_doors:
        door.get_prize()


def generate_door_list(count=10):
    """Генерация списка из дверей и его возврат"""
    return [Door() for _ in range(count)]


def pick_door(door_list: list[Door]) -> Door:
    """Выбор случайной двери и исключение ее из общего списка
    return door"""
    index = random.randrange(len(door_list))
    door = door_list.pop(index)
    return door


def get_closed_doors(door_list: list[Door], closed=1):
    """Возвращает список дверей которые будут закрыты"""
    close_doors = list(filter(lambda door: door.prize, door_list))
    close_doors.extend(
        random.sample(list(filter(lambda door: not door.prize, door_list)), closed - len(close_doors)))
    return close_doors


def valid_input_data(count_prize, count_door, closed_door):
    """Валидация принимаемых значений"""
    first = count_prize <= count_door - 2
    second = count_door - 1 > closed_door >= count_prize
    three = count_prize > 0 and count_door > 0 and closed_door > 0
    if all((first, second, three)):
        return True
    return False


def get_result(
        change=True,
        count_prize=10,
        count_door=30,
        closed_door=10,
        iteration=1000
):
    """Проведение эксперимента
    возвращает процент угаданных дверей за которыми был приз"""
    win = 0
    if valid_input_data(count_prize, count_door, closed_door):  # Проверка данных
        for i in range(iteration):  # iteration - количество экспериментов
            door_list = generate_door_list(count_door)  # генерация списка дверей
            put_the_prize(door_list, count_prize)  # Кладем приз за одну из дверей
            selected_door = pick_door(door_list)  # Выбираем случайную дверь
            close_door = get_closed_doors(door_list, closed_door)  # Оставляем закрытые двери
            if change:  # Выбор стратегии
                selected_door = pick_door(close_door)  # Меняем дверь на одну из закрытых
            win += selected_door.prize  # Если за выбранной дверью есть приз win += 1

        return round(win / iteration * 100, 2)  # Результат в процентах
    print("Ошибка данных")
    return False


def get_base_case(iteration=1000, change=True):
    """Возвращает результат классического случая"""
    return get_result(change=change, count_prize=1, count_door=3, closed_door=1, iteration=iteration)


def start_experiment(
        count_prize=10,
        count_door=30,
        closed_door=10,
        iteration=1000
):

    """Проведения двух экспериментов:
        - классический
        - пользовательский
    возвращает результаты двух экспериментов в виде словаря:
    "Base": data_base, "Customizable": data_other
    """
    data_base = {}
    data_other = {}
    for strat in strategy:
        if strat:
            strategy_name = "Change"
        else:
            strategy_name = "Stay"
        data_base[strategy_name] = get_base_case(change=strat)
        data_other[strategy_name] = get_result(change=strat, count_prize=count_prize, count_door=count_door,
                                               closed_door=closed_door,
                                               iteration=iteration)
    return {"Base": data_base, "Customizable": data_other}
