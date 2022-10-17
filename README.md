# Feuerverzinkung
41 Bundeswettbewerb Informatik

---
## Info:
- __Team-ID:__ *00080* 
- __Team:__ *If-Schleife*
- __Bearbeiter/-innen:__ *Richard Ewert*
- __Datum:__ *17. Oktober 2022*

---
## Lösungsidee
Die Simulation schreitet nur dann fort, wenn es durch ein Event ausgelöst wird,
um keine unnötigen Schritte zu berechnen.
Die Events haben einen Zeitpunkt, zu welchem sie eintreten.
Das jeweils frühste Event wird ausgeführt.
Es verändert den Zustand der Simulation und
erstellt die daraus folgenden weiteren Events.

---
## Umsetzung
Ein zweidimensionaler Numpy Array `crystal_image` der angegebenen größe wird mit Nullen gefüllt:
```crystal_image = np.zeros((size_y, size_x))```
Er repräsentiert den aktuellen Zustand der Simulation. Alle Felder sind Leer.

Eine verkettete Liste `events` enthält alle Events, welche noch auftreten.

Ein Event ist ein Objekt der Klasse `GrowthEvent`.
Es enthält alle wichtigen Informationen

---
## Beispiele

---
## Quellcode