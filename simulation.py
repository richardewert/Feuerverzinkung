import random


class Crystal:
    def __init__(self):
        resolution = 100
        self.up_time = random.randint(1, resolution)
        self.right_time = random.randint(1, resolution)
        self.down_time = random.randint(1, resolution)
        self.left_time = random.randint(1, resolution)

    def get_value(self, direction):
        if direction == "up":
            return self.up_time
        elif direction == "right":
            return self.right_time
        elif direction == "down":
            return self.down_time
        elif direction == "left":
            return self.left_time


def mk_matrix(size_x, size_y, init=-1):
    matrix = []
    for x in range(size_x):
        matrix.append([])
        for y in range(size_y):
            matrix[x].append(init)
    return matrix


def mk_crystals(amount):
    crystals = []
    for i in range(amount):
        crystals.append(Crystal())
    return crystals


def sort_evaluator(e):
    return e["time"]


def calculate_growth_order(crystals):
    order = []
    for crystal, i in zip(crystals, range(len(crystals))):
        order.append({"time": crystal.get_value("up"), "direction": "up", "crystal_index": i})
        order.append({"time": crystal.get_value("right"), "direction": "right", "crystal_index": i})
        order.append({"time": crystal.get_value("down"), "direction": "down", "crystal_index": i})
        order.append({"time": crystal.get_value("left"), "direction": "left", "crystal_index": i})
    order.sort(key=sort_evaluator)
    return order


def sprinkle_cristals(crystal_map, amount):
    cr_map = crystal_map
    size_x = len(crystal_map)
    size_y = len(crystal_map[0])
    for i in range(amount):
        x, y = random.randint(0, size_x), random.randint(0, size_y)
        while cr_map[x][y] != -1:
            x, y = random.randint(0, size_x), random.randint(0, size_y)
        cr_map[x][y] = i
    return cr_map


def grow(index, crystal_map):
    pass


def simulate(size_x=500, size_y=500, crystal_amount=50):
    crystal_map = mk_matrix(size_x, size_y, -1)

    crystals = mk_crystals(crystal_amount)
    growth_order = calculate_growth_order(crystals)

    crystal_map = sprinkle_cristals(crystal_map, crystal_amount)
    print(crystal_map)

    for i in range(100):
        current_time = growth_order[0]["time"]
        current_crystal_index = growth_order[0]["crystal_index"]
        current_direction = growth_order[0]["direction"]
        current_action = growth_order[0]

        del growth_order[0]
        grow(current_action["crystal_index"], crystal_map)

        for e in range(len(growth_order)):
            growth_order[e]["time"] = growth_order[e]["time"] - current_time

        new_action = current_action
        new_action["time"] = crystals[current_crystal_index].get_value(current_direction)
        readded = False
        e = 0
        while not readded and e < len(growth_order):
            if growth_order[e]["time"] > new_action["time"]:
                growth_order.append(new_action)
                readded = True
            e += 1
        if not readded:
            growth_order.append(new_action)


if __name__ == "__main__":
    simulate(size_x=500, size_y=500, crystal_amount=50)
