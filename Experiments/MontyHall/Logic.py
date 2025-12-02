import random


class Door:
    def __init__(self, prize=False):
        self.prize = prize

    def get_prize(self):
        self.prize = True


strategy = (True, False)


def put_the_prize(door_list: list[Door], count_prize=1):
    choice_doors = random.sample(door_list, count_prize)
    for door in choice_doors:
        door.get_prize()


def generate_door_list(count=10):
    return [Door() for _ in range(count)]


def pick_door(door_list: list[Door]) -> Door:
    index = random.randrange(len(door_list))
    door = door_list.pop(index)
    return door


def get_closed_doors(door_list: list[Door], closed=1):
    close_doors = list(filter(lambda door: door.prize, door_list))
    close_doors.extend(
        random.sample(list(filter(lambda door: not door.prize, door_list)), closed - len(close_doors)))
    return close_doors


def valid_input_data(count_prize, count_door, closed_door):
    first = count_prize <= count_door - 2
    second = count_door - 1 > closed_door >= count_prize
    three = count_prize > 0 and count_door > 0 and closed_door > 0
    if all((first, second, three)):
        return True
    return False


def get_result(change=True, count_prize=10, count_door=30, closed_door=10, iteration=1000):
    win = 0
    if valid_input_data(count_prize, count_door, closed_door):
        for i in range(iteration):
            door_list = generate_door_list(count_door)
            put_the_prize(door_list, count_prize)
            selected_door = pick_door(door_list)
            close_door = get_closed_doors(door_list, closed_door)
            if change:
                selected_door = pick_door(close_door)
            win += selected_door.prize

        return round(win / iteration * 100, 2)
    print("Ошибка данных")
    return False


def get_base_case(iteration=1000, change=True):
    return get_result(change=change, count_prize=1, count_door=3, closed_door=1, iteration=iteration)


def start_experiment(count_prize=10, count_door=30, closed_door=10, iteration=1000):
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
