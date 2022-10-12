import random
from PIL import Image

SIZE_X = 200
SIZE_Y = 200


class Crystal:
    def __init__(self):
        resolution = 60
        self.up_time = random.randint(50, resolution)
        self.right_time = random.randint(50, resolution)
        self.down_time = random.randint(50, resolution)
        self.left_time = random.randint(50, resolution)

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


def render(crystal_map, name):
    img = Image.new('RGB', (SIZE_X, SIZE_Y), "black")
    pixels = img.load()
    for f in range(img.size[0]):
        for j in range(img.size[1]):
            v = clamp(crystal_map[f - 1][j - 1] * 5, 0, 255)
            pixels[f - 1, j - 1] = (v, v, v)
    img.save(tr(name) + ".png")


def is_clamp(value, low, high):
    return value > high or value < low


def eval(x):
    return x["time"]


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


def calculate_growth_order(crystals) -> []:
    order = []
    for crystal, i in zip(crystals, range(len(crystals))):
        order.append({"time": crystal.get_value("up"), "direction": "up", "crystal_index": i})
        order.append({"time": crystal.get_value("right"), "direction": "right", "crystal_index": i})
        order.append({"time": crystal.get_value("down"), "direction": "down", "crystal_index": i})
        order.append({"time": crystal.get_value("left"), "direction": "left", "crystal_index": i})
    order.sort(key=eval)
    return order


def sprinkle_cristals(crystal_map, amount):
    new_map = crystal_map
    size_x = SIZE_X - 1
    size_y = SIZE_Y - 1
    for i in range(amount):
        x, y = random.randint(0, size_x), random.randint(0, size_y)
        while new_map[x][y] != -1:
            x, y = random.randint(0, size_x), random.randint(0, size_y)
        new_map[x][y] = i
    return new_map


def quick_grow(index, direction, crystal_map):
    offset_x, offset_y = 0, 0
    if direction == "up":
        offset_x, offset_y = 0, 1
    elif direction == "right":
        offset_x, offset_y = 1, 0
    elif direction == "down":
        offset_x, offset_y = 0, -1
    elif direction == "left":
        offset_x, offset_y = -1, 0

    growing_crystals = []
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            if crystal_map[x][y] == index:
                growing_crystals.append({"x": x, "y": y})

    for crystal in growing_crystals:
        goal_field_x = crystal["x"] + offset_x
        goal_field_y = crystal["y"] + offset_y
        if not (is_clamp(goal_field_x, 0, SIZE_X - 1) or is_clamp(goal_field_y, 0, SIZE_Y - 1)):
            if crystal_map[goal_field_x][goal_field_y] == -1:
                crystal_map[goal_field_x][goal_field_y] = index

    return crystal_map


def simulate(crystal_amount=50, iterations=1000):
    crystal_map = mk_matrix(SIZE_X, SIZE_Y, -1)

    crystals = mk_crystals(crystal_amount)
    growth_order = calculate_growth_order(crystals)

    crystal_map = sprinkle_cristals(crystal_map, crystal_amount)

    for i in range(iterations):
        # Wachstumsaktion durchführen
        crystal_map = quick_grow(growth_order[0]["crystal_index"], growth_order[0]["direction"], crystal_map)

        # Zeit aktueller Aktion von allen anderen abziehen
        length = len(growth_order) - 1
        for e in range(length):
            growth_order[length - e]["time"] -= growth_order[0]["time"]

        # Zeit für ausgeführte Aktion zurücksetzten
        growth_order[0]["time"] = crystals[growth_order[0]["crystal_index"]].get_value(growth_order[0]["direction"])

        # Sortieren
        growth_order = sorted(growth_order, key=lambda x: x["time"])
        # growth_order.sort(key=eval)

        print(str(round((i / iterations) * 100 * 10) / 10) + "%")

    # Bild erstellen
    render(crystal_map, 0)


if __name__ == "__main__":
    simulate(crystal_amount=50, iterations=10000)
