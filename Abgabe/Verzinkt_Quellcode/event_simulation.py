import collections      # Für verkettete Listen
import random           # Für zufällige Initialisierung der Kristalle
import numpy as np      # Für bessere Arrays

from numpy import array
from tqdm import tqdm   # Für schöne Fortschrittsanzeige
from PIL import Image   # Um das Bild zu erstellen

# Verkettete Liste mit Wachstumsevents für schnellere Sortierung
events = collections.deque()
# Größe der Simulation und des resultierenden Bildes
size_x = 250
size_y = 250
# Anzahl an Kristallen wird auf 1 pro 100 pixel festgelegt
cristal_amount = round(size_x*size_y/100)
# Numpy Array mit der richtigen größe, enthält Kristall Farben
crystal_image = np.zeros((size_y, size_x))
# Anzahl der bereits von Kristallen gefüllten Pixel, nötig für Fortschrittsanzeige
simulated_pixels = 0


class GrowthEvent:
    def __init__(self, time_offsets: [], time: float, position: [], color: int) -> None:
        """
        Initialisiert einen neues Kristallwachstumsevent

        :param time_offsets: Ein Array mit 4 Werten, für jede Richtung einen, mit der jeweiligen Zeit zwischen den Wachstumschritten
        :param time: Der Zeitpunkt, zu dem das Event eintreten soll
        :param position: die Position, die vom Event verändert werden soll
        :param color: die Farbe, die der Kristall haben soll
        """
        self.time_offsets: [] = time_offsets
        self.time: float = time
        self.position: [] = position
        self.color: int = color


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
    # Für jeden zu erstellenden Kristall jeweils:
    for i in range(amount):
        # Eine zufällige Position zuweisen bis eine gefunden wird an der noch kein Kristall ist
        position = [random.randint(0, size_y - 1), random.randint(0, size_x - 1)]
        while position in used_positions:
            position = [random.randint(0, size_y - 1), random.randint(0, size_x - 1)]
        used_positions.append(position)
        # Die Zeiten, welche für die jeweilige Richtung bis zum nächsten Wachstum benötigt wird, zufällig festlegen
        time_offsets = [
            random.randint(min_time, max_time),
            random.randint(min_time, max_time),
            random.randint(min_time, max_time),
            random.randint(min_time, max_time)
        ]
        # Eine Farbe für den Kristall festlegen, das Objekt erstellen und in die Liste einfügen.
        new_events.append(GrowthEvent(time_offsets=time_offsets, time=0, position=position, color=random.randint(50, 255)))
    return new_events


def render(crystals: array, name: any = "result") -> None:
    """
    Stellt den Numpy Array als Bild dar und speichert es unter dem angegebenem Namen ab

    :param crystals: Der Numpy Array mit den Kristall Farben
    :param name: Der Name des Bildes
    :return: Nichts
    """
    im = Image.fromarray(crystals)  # In Pillow Bild umwandeln
    im = im.convert("L")            # Farbraum festlegen
    im.show()                       # Bild anzeigen
    im.save(str(name) + ".png")     # Bild abspeichern


def fire(event: GrowthEvent) -> None:
    """
    Führt ein Wachstumsevent durch, erstellt die daraus Folgenden und sortiert sie an die richtigen Stellen ein

    :param event: Das durchzuführende Wachstumsevent
    :return: Nichts
    """
    # Nur Falls die zu schreibende Position noch nicht belegt ist:
    if crystal_image[event.position[0]][event.position[1]] == 0:
        # Den Wert in der Matrix, an der richtigen Position, auf den Farbwert des Events setzen
        crystal_image[event.position[0]][event.position[1]] = event.color

        global simulated_pixels     # Globale Variable im Namespace bekannt machen
        simulated_pixels += 1       # Anzahl schon veränderter Pixel um 1 erhöhen

        # Eine Liste aller Positionen, an denen ein neues Event auftreten muss, erstellen
        positions = [
            [event.position[0] + 0, event.position[1] + 1],
            [event.position[0] + 0, event.position[1] + -1],
            [event.position[0] + 1, event.position[1] + 0],
            [event.position[0] + -1, event.position[1] + 0]
        ]
        for position, direction in zip(positions, range(4)):                # Jede dieser Positionen
            if size_y > position[0] >= 0 and size_x > position[1] >= 0:     # wird, falls sie innerhalb der Simulation liegen,
                if crystal_image[position[0]][position[1]] == 0:            # und noch nicht belegt sind
                    new_event = GrowthEvent(event.time_offsets, event.time + event.time_offsets[direction], position, event.color)
                    events.append(new_event)                                # als Teil eines neuen Events in die Event-Liste geschrieben
        events.sort(key=lambda x: x.time)   # Die Event-Liste wird nach Zeit sortiert


if __name__ == "__main__":
    events = init_events(amount=cristal_amount)  # Seed-Kristalle werden initialisiert
    for i in tqdm(range(size_x * size_y)):                  # Für die Menge an Pixeln im Bild (nötig für Fortschrittsanzeige)
        old_simulated = simulated_pixels
        while simulated_pixels <= old_simulated:            # Solange es keine Veränderung im Bild gibt
            fire(events.pop(0))                             # Wird das unterste Event, also das mit der geringsten Zeit, ausgeführt und aus der Liste entfernt

    render(crystal_image, f"x{size_x}y{size_y}a{cristal_amount}" + f"_{0}")
