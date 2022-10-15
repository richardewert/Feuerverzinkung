import collections
import logging
import random
from tqdm import tqdm

import numpy as np
from PIL import Image
from numpy import array

events = collections.deque()
size_x = 1920
size_y = 1080
crystal_image = np.zeros((size_y, size_x))
simulated_pixels = 0


def init_events(amount=50, min_time=50, max_time=100):
    new_events = []
    used_positions = []
    for i in range(amount):
        position = [random.randint(0, size_y - 1), random.randint(0, size_x - 1)]
        while position in used_positions:
            position = [random.randint(0, size_y - 1), random.randint(0, size_x - 1)]
        used_positions.append(position)
        time_offsets = [
            random.randint(min_time, max_time),
            random.randint(min_time, max_time),
            random.randint(min_time, max_time),
            random.randint(min_time, max_time)
        ]
        new_events.append(GrowthEvent(time_offsets=time_offsets, time=0, direction=0, position=position,
                                      color=random.randint(50, 255)))
    new_events.sort(key=lambda x: x.time)
    return new_events


def render(crystals, name):
    im = array(crystals)
    im = Image.fromarray(im)
    im = im.convert("L")
    im.show()
    im.save(str(name) + ".png")


class GrowthEvent:
    def __init__(self, time_offsets: [], time: int, direction: int, position: [], color: int):
        self.time_offsets: [] = time_offsets
        self.time: int = time + time_offsets[direction]
        self.position: [] = position
        self.color: int = color


def fire(event):
    if crystal_image[event.position[0]][event.position[1]] == 0:
        crystal_image[event.position[0]][event.position[1]] = event.color
        global simulated_pixels
        simulated_pixels += 1

        positions = [
            [event.position[0] + 0, event.position[1] + 1],
            [event.position[0] + 0, event.position[1] + -1],
            [event.position[0] + 1, event.position[1] + 0],
            [event.position[0] + -1, event.position[1] + 0]
        ]
        for position, direction in zip(positions, range(4)):
            if size_y > position[0] >= 0 and size_x > position[1] >= 0:
                if crystal_image[position[0]][position[1]] == 0:
                    new_event = GrowthEvent(event.time_offsets, event.time, direction, position, event.color)
                    events.append(new_event)
        events.sort(key=lambda x: x.time)


if __name__ == "__main__":
    events = init_events(amount=round(size_x*size_y/1000))
    for i in tqdm(range(size_x * size_y)):
        old_simulated = simulated_pixels
        while simulated_pixels <= old_simulated:
            fire_sort(events.pop(0))
            logging.debug(crystal_image)

    render(crystal_image, "result")
