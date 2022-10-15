import logging
import random
from tqdm import tqdm

import numpy as np
from PIL import Image
from numpy import array

events = []
size_x = 500
size_y = 500
crystal_image = np.zeros((size_y, size_x))
simulated_pixels = 10


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
    Image.fromarray(im).show()


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
            if size_x > position[0] >= 0 and size_y > position[1] >= 0:
                if crystal_image[position[0]][position[1]] == 0:
                    object = GrowthEvent(event.time_offsets, event.time, direction, position, event.color)
                    done = False
                    j = 0
                    time = event.time + event.time_offsets[direction]
                    while not done:
                        if j < len(events):
                            if events[j].time > time:
                                events.insert(j, object)
                                done = True
                            if events[j].position == position:
                                done = True
                            j += 1
                        else:
                            events.append(object)
                            done = True


def fire_sort(event):
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
            if size_x > position[0] >= 0 and size_y > position[1] >= 0:
                if crystal_image[position[0]][position[1]] == 0:
                    object = GrowthEvent(event.time_offsets, event.time, direction, position, event.color)
                    events.append(object)
        events.sort(key=lambda x: x.time)


if __name__ == "__main__":
    events = init_events()
    for i in tqdm(range(size_x * size_y)):
        old_simulated = simulated_pixels
        while simulated_pixels <= old_simulated:
            fire(events.pop(0))
            logging.debug(crystal_image)

    render(crystal_image, "result")
