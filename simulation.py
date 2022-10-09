import copy
import random
from PIL import Image


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


def clamp(value, low, high):
    if value >= high:
        return high
    elif value <= low:
        return low
    else:
        return value


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
    sorted(order, key=lambda x: x["time"])
    return order


def sprinkle_cristals(crystal_map, amount):
    new_map = crystal_map
    size_x = len(crystal_map) - 1
    size_y = len(crystal_map[0]) - 1
    for i in range(amount):
        x, y = random.randint(0, size_x), random.randint(0, size_y)
        while new_map[x][y] != -1:
            x, y = random.randint(0, size_x), random.randint(0, size_y)
        new_map[x][y] = i
    return new_map


def grow(index, direction, crystal_map: []):
    # new_map = copy.deepcopy(crystal_map)
    # new_map = crystal_map
    new_map = []
    for x in range(len(crystal_map)):
        new_map.append([])
        for y in range(len(crystal_map[0])):
            new_map[x].append(crystal_map[x][y])

    offset_x, offset_y = 0, 0
    if direction == "up":
        offset_x, offset_y = 0, 1
    elif direction == "right":
        offset_x, offset_y = 1, 0
    elif direction == "down":
        offset_x, offset_y = 0, -1
    elif direction == "left":
        offset_x, offset_y = -1, 0

    size_x = len(crystal_map)
    size_y = len(crystal_map[0])
    for row, x in zip(crystal_map, range(size_x)):
        for item, y in zip(row, range(size_y)):
            if item == index:
                check_x, check_y = clamp(x + offset_x, 0, size_x - 1), clamp(y + offset_y, 0, size_y - 1)
                if crystal_map[check_x][check_y] == -1:
                    new_map[check_x][check_y] = index
    return new_map


def simulate(size_x=500, size_y=500, crystal_amount=50, iterations=1000):
    crystal_map = mk_matrix(size_x, size_y, -1)

    crystals = mk_crystals(crystal_amount)
    growth_order = calculate_growth_order(crystals)

    crystal_map = sprinkle_cristals(crystal_map, crystal_amount)

    for i in range(iterations):
        # Wachstumsaktion durchführen
        crystal_map = grow(growth_order[0]["crystal_index"], growth_order[0]["direction"], crystal_map)

        # Zeit aktueller Aktion von allen anderen abziehen
        for e in range(len(growth_order)):
            growth_order[e]["time"] = growth_order[e]["time"] - growth_order[0]["time"]

        # Zeit für ausgeführte Aktion zurücksetzten
        growth_order[0]["time"] = crystals[growth_order[0]["crystal_index"]].get_value(growth_order[0]["direction"])

        # Sortieren
        sorted(growth_order, key=lambda x: x["time"])

        print(str(round((i / iterations) * 100 * 10) / 10) + "%")

    img = Image.new('RGB', (size_x, size_y), "black")
    pixels = img.load()
    for f in range(img.size[0]):
        for j in range(img.size[1]):
            v = clamp(crystal_map[f - 1][j - 1] * 5, 0, 255)
            pixels[f, j] = (v, v, v)
    img.save("test" + str(0) + ".png")


if __name__ == "__main__":
    simulate(size_x=500, size_y=500, crystal_amount=50, iterations=10000)
