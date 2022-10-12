import copy
import random
from PIL import Image

SIZE_X = 200
SIZE_Y = 200
MIN_TIME = 50
MAX_TIME = 100


def is_clamping(value: float, low: float, high: float) -> bool:
    return value > high or value < low


def render(crystal_map, name: any = 0):
    img = Image.new('RGB', (SIZE_X, SIZE_Y), "black")
    pixels: [] = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            v = 0
            crystal = crystal_map[i][j]
            if crystal is not None:
                v = crystal["color"]
            pixels[i, j] = (v, v, v)
    img.save(str(name) + ".png")


def mk_matrix(size_x: int, size_y: int, init: any = None) -> []:
    matrix = []
    for x in range(size_x):
        matrix.append([])
        for y in range(size_y):
            matrix[x].append(init)
    return matrix


def mk_crystal(color, times, x, y):
    return {
        "color": color,
        "max_times": copy.deepcopy(times),
        "current_times": times,
        "x": x,
        "y": y
    }


def sprinkle_cristals(crystal_map: [], amount: int) -> []:
    size_x, size_y = SIZE_X - 1, SIZE_Y - 1
    for i in range(amount):
        x, y = random.randint(0, size_x), random.randint(0, size_y)
        while crystal_map[x][y] is not None:
            x, y = random.randint(0, size_x), random.randint(0, size_y)
        times = [
            random.randint(MIN_TIME, MAX_TIME),
            random.randint(MIN_TIME, MAX_TIME),
            random.randint(MIN_TIME, MAX_TIME),
            random.randint(MIN_TIME, MAX_TIME)
        ]
        crystal_map[x][y] = mk_crystal(random.randint(50, 200), times, x, y)
    return crystal_map


def filled(crystal_map):
    amount = 0
    for row in crystal_map:
        for i in row:
            if i is not None:
                amount += 1
    return amount - (SIZE_X*SIZE_Y)


def grow(growing, time, crystal_map):
    for crystal in growing:
        for current_time, i in zip(crystal["current_times"], range(4)):
            if current_time == time:
                offset_x, offset_y = 0, 0
                if i == 0:
                    offset_x, offset_y = 0, 1
                elif i == 1:
                    offset_x, offset_y = 1, 0
                elif i == 2:
                    offset_x, offset_y = 0, -1
                elif i == 3:
                    offset_x, offset_y = -1, 0

                goal_field_x = crystal["x"] + offset_x
                goal_field_y = crystal["y"] + offset_y
                if not (is_clamping(goal_field_x, 0, SIZE_X - 1) or is_clamping(goal_field_y, 0, SIZE_Y - 1)):
                    if crystal_map[goal_field_x][goal_field_y] is None:

                        crystal_map[goal_field_x][goal_field_y] = mk_crystal(crystal["color"], crystal["max_times"],
                                                                             goal_field_x, goal_field_y)


def get_growing(crystal_map):
    smallest_time = 10000
    growing = []
    for row in crystal_map:
        for crystal in row:
            if crystal is not None:
                for time in crystal["current_times"]:
                    if time < smallest_time:
                        smallest_time = time
                        growing = [crystal]
                    elif time == smallest_time:
                        growing.append(crystal)
    return growing, smallest_time


def subtract_time(crystal_map, subtraction_time):
    for row in crystal_map:
        for crystal in row:
            if crystal is not None:
                for time, i in zip(crystal["current_times"], range(4)):
                    crystal["current_times"][i] -= subtraction_time
                    if time == 0:
                        crystal["current_times"][i] = crystal["max_times"][i]


def simulate():
    crystal_map = mk_matrix(SIZE_X, SIZE_Y)
    crystal_map = sprinkle_cristals(crystal_map, 50)

    fill = filled(crystal_map)
    while fill != 0:
        growing, smallest_time = get_growing(crystal_map)

        grow(growing, smallest_time, crystal_map)

        subtract_time(crystal_map, smallest_time)

        fill = filled(crystal_map)
        print(fill)

    render(crystal_map)


if __name__ == "__main__":
    simulate()
