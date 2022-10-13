from PIL import Image

EVENTS = []
CRYSTALS = []
SIZE_X = 200
SIZE_Y = 200
TIME = 0

class GrowthEvent:
    def __init__(self, time_offsets: [], time: int, direction: int, position: [], color: int):
        self.time_offsets: [] = time_offsets
        self.time: int = time + time_offsets[direction]
        self.position: [] = position
        self.color: int = color

    def fire(self):
        if not any(d["position"] == self.position for d in CRYSTALS):
            CRYSTALS.append({"position": self.position, "color": self.color})

        positions = [
            [self.position[0] + 0, self.position[1] + 1],
            [self.position[0] + 0, self.position[1] + -1],
            [self.position[0] + 1, self.position[1] + 0],
            [self.position[0] + -1, self.position[1] + 0]
        ]
        for position, direction in zip(positions, range(4)):
            EVENTS.append(GrowthEvent(self.time_offsets, self.time, direction, position, self.color))


if __name__ == "__main__":
    EVENTS.append(GrowthEvent(time_offsets=[10, 5, 7, 8], time=0, direction=1, position=[10, 9], color=1))
    while len(EVENTS) > 0:
        EVENTS[0].fire()
        EVENTS.pop(0)
        EVENTS = EVENTS.sort(key=lambda x: x.time)

    print(CRYSTALS)

