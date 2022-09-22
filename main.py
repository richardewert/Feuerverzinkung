from random import randint
from vector import Vec2


class Cristal:
    def __init__(self, origin: Vec2):
        self.position: Vec2 = origin


class Tile:
    def __init__(self, position: Vec2, content=None):
        self.position: Vec2 = position
        self.content = content

    def set_content(self, content):
        self.content = content


class Simulation:
    def __init__(self, size: Vec2 = Vec2(500, 500), seeds: int = 500):
        """
        Enthält alle für die Simulation nötigen Informationen und führt die Simulationsschritte aus.
        :param size: Die größe der Simulation
        :param seeds: Die Anzahl an Kristallkernen
        """
        self.size: Vec2 = size
        self.seed_amount: int = seeds

        self.step = None
        self.state = None
        self.crystals = []
        self.restart()
        self.generate_crystals()

    def restart(self):
        self.step = 0
        self.clear()

    def clear(self):
        size = self.size
        self.state = []
        for x in range(size.x):
            self.state.append([])
            for y in range(size.y):
                self.state[x].append(Tile(Vec2(x, y)))

    def generate_crystals(self, amount: int = 500):
        size = self.size
        for i in range(amount):
            pos = Vec2(randint(0, size.x - 1), randint(0, size.y - 1))
            self.crystals.append(Cristal(pos))
            self.state[pos.x][pos.y].set_content(self.crystals[len(self.crystals) - 1])


if __name__ == "__main__":
    state = Simulation()
    print(state.state)
