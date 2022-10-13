from PIL import Image

EVENTS = []
CRYSTALS = []
SIZE_X = 200
SIZE_Y = 200
TIME = 0


def render(crystals, name):
    img = Image.new('RGB', (SIZE_X, SIZE_Y), "black")
    pixels = img.load()
    for crystal in crystals:
        pos = crystal["position"]
        v = crystal["color"]
        pixels[pos[0], pos[0]] = (v, v, v)
    img.save(str(name) + ".png")
    print("save")


class GrowthEvent:
    def __init__(self, time_offsets: [], time: int, direction: int, position: [], color: int):
        self.time_offsets: [] = time_offsets
        self.time: int = time + time_offsets[direction]
        self.position: [] = position
        self.color: int = color

    def fire(self, i: int):
        if not any(d["position"] == self.position for d in CRYSTALS):
            CRYSTALS.append({"position": self.position, "color": self.color})

            positions = [
                [self.position[0] + 0, self.position[1] + 1],
                [self.position[0] + 0, self.position[1] + -1],
                [self.position[0] + 1, self.position[1] + 0],
                [self.position[0] + -1, self.position[1] + 0]
            ]
            for position, direction in zip(positions, range(4)):
                if not any(d["position"] == position for d in CRYSTALS):
                    EVENTS.append(GrowthEvent(self.time_offsets, self.time, direction, position, self.color))
            EVENTS.sort(key=lambda x: x.time)
        if i <= 979:
            EVENTS[EVENTS.index(self) + 1].fire(i + 1)


if __name__ == "__main__":
    EVENTS.append(GrowthEvent(time_offsets=[10, 5, 7, 8], time=0, direction=1, position=[0, 0], color=200))
    EVENTS[0].fire(0)

    print("success")
    render(CRYSTALS, 0)

