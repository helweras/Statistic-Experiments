import random
from Experiments.PlaygroundParadox.Components import ChildHouse
from Experiments.PlaygroundParadox.Components.casino_terminal import casino


class BloodTiles:

    @staticmethod
    def family_connect(child_list: list):
        check = [child_list[0].second_name]
        for child in child_list[1:]:
            if child.second_name in check:
                return True
            else:
                check.append(child.second_name)
        return False

    @staticmethod
    def get_class(all_children, value):
        return random.sample(all_children, value)

    def start_simulate(self, post_data):

        weight = post_data["weight"]
        value = post_data["value"]
        count_sim = post_data["count_sim"]
        num_of_family = post_data["num_of_family"]

        counter = 0

        child_house = ChildHouse(weights_born=weight,
                                 count_family=num_of_family
                                 )

        all_children = child_house.all_children_list

        for _ in range(count_sim):
            result = self.get_class(all_children=all_children,
                                    value=value
                                    )
            if self.family_connect(result):
                counter += 1

        data = {"result": round(counter / count_sim * 100, 2)}

        return data
