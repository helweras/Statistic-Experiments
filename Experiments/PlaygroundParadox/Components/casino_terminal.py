import random


def gen_random_weight():
    points = sorted([random.randrange(101) for _ in range(4)])
    points = [0] + points + [100]

    weights = tuple(next_val - current for current, next_val in zip(points, points[1:]))

    return weights


def get_random_value(start=7, stop=22):
    return random.randrange(start, stop)


def win(real, prog, stav):
    if abs(real - prog) <= 2:
        return stav * 5
    elif 2 < abs(real - prog) <= 10:
        return stav * 2
    elif 10 < abs(real-prog) <= 20:
        return stav
    else:
        return 0



def casino(coin, blood_tiles_fun):
    dk = coin

    while dk > 0:
        post_request = {
            "weight": (8, 22, 55, 6, 9),
            "value": 15,
            "count_sim": 10000,
            "num_of_family": 100
        }
        print(f"dk = {dk}")
        print("распределение")
        print(post_request["weight"])
        print("размер группы = ", post_request["value"])
        stavka = int(input("ваша ставка - "))
        while stavka > dk:
            stavka = int(input("ваша ставка - "))
        dk -= stavka
        your_num = int(input("ваш прогноз - "))
        real = blood_tiles_fun(post_request)["result"]
        print(f"real = {real}\nyour = {your_num}")
        dk += win(real=real, prog=your_num, stav=stavka)
        print(f"your dk = {dk}")
        input("Нажми Enter что бы продолжить")
        print("=================================")
    print("end")


