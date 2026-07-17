import random


class Door:
    """Класс описывающий состояние двери"""

    def __init__(self, prize=False):
        self.prize = prize  # есть ли приз за дверью

    def get_prize(self):
        """Присваивает True self.prize"""
        self.prize = True




class Simulate:
    strategy = (True, False)  # Стратегии менять, не менять

    @staticmethod
    def put_the_prize(door_list: list[Door], count_prize=1):
        """Случайным дверям в атрибут self.prize присваивается значение True
        Количество дверей определяется count_prize"""
        choice_doors = random.sample(door_list, count_prize)
        for door in choice_doors:
            door.get_prize()

    @staticmethod
    def generate_door_list(count=10):
        """Генерация списка из дверей и его возврат"""
        return [Door() for _ in range(count)]

    @staticmethod
    def pick_door(door_list: list[Door]) -> Door:
        """Выбор случайной двери и исключение ее из общего списка
        return door"""
        index = random.randrange(len(door_list))
        door = door_list.pop(index)
        return door

    @staticmethod
    def open_door(door_list: list[Door], count_open=1):
        open_doors = random.sample(list(filter(lambda door: not door.prize, door_list)), count_open)
        pass

    @staticmethod
    def get_closed_doors(door_list: list[Door], closed=1):
        """Возвращает список дверей которые будут закрыты"""
        close_doors = list(filter(lambda door: door.prize, door_list))
        close_doors.extend(
            random.sample(list(filter(lambda door: not door.prize, door_list)), closed - len(close_doors)))
        return close_doors

    @staticmethod
    def valid_input_data(count_prize, count_door, closed_door):
        """Валидация принимаемых значений"""
        first = count_prize <= count_door - 2
        second = count_door - 1 > closed_door >= count_prize
        three = count_prize > 0 and count_door > 0 and closed_door > 0
        if all((first, second, three)):
            return True
        return False

    def get_result(self,
            change=True,
            count_prizes=10,
            count_doors=30,
            closed_doors=10,
            iteration=1000
    ):
        """Проведение эксперимента
        возвращает процент угаданных дверей за которыми был приз"""
        win = 0
        for i in range(iteration):  # iteration - количество экспериментов
            door_list = self.generate_door_list(count_doors)  # генерация списка дверей
            self.put_the_prize(door_list, count_prizes)  # Кладем приз за одну из дверей
            selected_door = self.pick_door(door_list)  # Выбираем случайную дверь
            close_door = self.get_closed_doors(door_list, closed_doors)  # Оставляем закрытые двери
            if change:  # Выбор стратегии
                selected_door = self.pick_door(close_door)  # Меняем дверь на одну из закрытых
            win += selected_door.prize  # Если за выбранной дверью есть приз win += 1

        return round(win / iteration * 100, 2)  # Результат в процентах


    def get_base_case(self, iteration=1000, change=True):
        """Возвращает результат классического случая"""
        return self.get_result(change=change, count_prizes=1, count_doors=3, closed_doors=1, iteration=iteration)

    def start_simulate(self,
            count_prizes=1,
            count_doors=3,
            closed_doors=1,
            iterable=175
    ):


        """
        возвращает результат эксперимента:
        """
        data = {}
        for strat in self.strategy:
            if strat:
                strategy_name = "Change"
            else:
                strategy_name = "Stay"
            data[strategy_name] = self.get_result(change=strat, count_prizes=count_prizes, count_doors=count_doors,
                                                   closed_doors=closed_doors,
                                                   iteration=iterable)
        return {"data_experiments": data}

