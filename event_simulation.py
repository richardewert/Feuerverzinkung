import collections
import random

import numpy
from tqdm import tqdm

import numpy as np
from PIL import Image
from numpy import array

events = collections.deque()
size_x = 250
size_y = 250
crystal_image = np.zeros((size_y, size_x))
simulated_pixels = 0


def init_events(amount=50, min_time=50, max_time=100) -> []:
    """
    Initialisiert die ersten Kristalle in Form von Wachstumsevents
    :param amount: Die Anzahl an hin zuzufügenden Kristallen
    :param min_time: Die minimale Zeit, die ein Kristall bis zum nächsten Wachstumsschritt benötigt
    :param max_time: Die maximale Zeit, die ein Kristall bis zum nächsten Wachstumsschritt benötigt
    :return: eine Liste von Wachstumsevents, an zufälligen stellen, zu zufälligen Zeiten innerhalb der Begrenzungen
    """
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
        new_events.append(GrowthEvent(time_offsets=time_offsets, time=0, position=position, color=random.randint(50, 255)))
    new_events.sort(key=lambda x: x.time)
    return new_events


def render(crystals: numpy.array, name: any = "result") -> None:
    """
    Stellt den Numpy Array als Bild dar und speichert es unter dem angegebenem Namen ab

    :param crystals: Der Numpy Array mit den Kristall Farben
    :param name: Der Name des Bildes
    :return: Nichts
    """
    im = array(crystals)
    im = Image.fromarray(im)
    im = im.convert("L")
    im.show()
    im.save(str(name) + ".png")


class GrowthEvent:
    def __init__(self, time_offsets: [], time: int, position: [], color: int) -> None:
        """
        Initialisiert einen neues Kristallwachstumsevent

        :param time_offsets: Ein Array mit 4 Werten, für jede Richtung einen, mit der jeweiligen Zeit zwischen den Wachstumschritten
        :param time: Der Zeitpunkt, zu dem das Event eintreten soll
        :param position: die Position, die vom Event verändert werden soll
        :param color: die Farbe, die der Kristall haben soll
        """
        self.time_offsets: [] = time_offsets
        self.time: int = time
        self.position: [] = position
        self.color: int = color


def fire(event: GrowthEvent) -> None:
    """
    Führt ein Wachstumsevent durch, erstellt die daraus Folgenden und sortiert sie an die richtigen Stellen ein

    :param event: Das durchzuführende Wachstumsevent
    :return: Nichts
    """
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
                    new_event = GrowthEvent(event.time_offsets, event.time + event.time_offsets[direction], position, event.color)
                    events.append(new_event)
        events.sort(key=lambda x: x.time)


if __name__ == "__main__":
    events = init_events(amount=round(size_x*size_y/1000))
    for i in tqdm(range(size_x * size_y)):
        old_simulated = simulated_pixels
        while simulated_pixels <= old_simulated:
            fire(events.pop(0))

    render(crystal_image, "result")
