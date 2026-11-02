import os
import random

from text import coord

class Station:
    x = 0
    y = 0
    name = ""
    major = False
    letter = "?"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.major = random.choice((True, False))

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return self.letter.lower() if not self.major else self.letter.upper()

    def verbose(self):
        return f'{self.name} ({self}): {coord(self.x)}/{coord(self.y)}'

class Residential(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.letter = "r"

class Commercial(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.letter = "c"

class Industrial(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.letter = "i"

class Medical(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.letter = "m"

class Entertainment(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.letter = "e"

class Park(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.letter = "p"

def randomStation(x, y):
    return random.choices((Residential(x, y), Commercial(x, y), Industrial(x, y), Medical(x, y), Entertainment(x, y), Park(x, y)), (10, 5, 5, 3, 3, 3))[0]

class Game:
    clear_cmd = ""
    board_size = 20
    stations = []
    running = True
    state = "MAP"

    def __init__(self, clear_cmd, board_size):
        self.clear_cmd = clear_cmd
        self.board_size = board_size

    def clear(self):
        os.system(self.clear_cmd)

    def new_position(self):
        if len(self.stations) == 0:
            return (self.board_size // 2, self.board_size // 2)
        found = False
        x = 0
        y = 0
        while not found:
            station: Station = random.choice(self.stations)
            x = min(max(station.x + random.randint(-3, 3), 0), self.board_size - 1)
            y = min(max(station.x + random.randint(-3, 3), 0), self.board_size - 1)
            found = True
            for existing in self.stations:
                if existing.x == x and existing.y == y: found = False
        return (x, y)

    def print_map(self):
        padding = len(coord(self.board_size))

        for row in range(padding):
            print(padding * " ", end="")
            for i in range(self.board_size):
                padded = f'{coord(i):>{padding}}'
                print(" " + padded[row], end="")
            print("")

        for y in range(self.board_size):
            padded = f'{coord(y):>{padding}}'
            print(padded, end="")
            for x in range(self.board_size):
                print(" ", end="")
                found = False
                for station in self.stations:
                    if station.x == x and station.y == y:
                        print(station, end="")
                        found = True
                if not found: print(" ", end="")
            print("")

    def new_station(self):
        position = self.new_position()
        station = randomStation(position[0], position[1])
        self.stations.append(station)
        self.clear()
        self.print_map()
        name = input(f'New Station{station.verbose()}. Enter a name for the Station: ')
        self.stations[-1].set_name(name)
        self.clear()
        self.print_map()

    def run(self):
        self.clear()

        while self.running:
            self.new_station()
            self.state = "MAP"
            while not self.state == "DAY":
                match self.state:

                    case "MAP":
                        action = "?"
                        while action not in "dlsx":
                            action = input("What do you want to do? (d: Simulate Day, l: Line Editor, s: List Stations, x: Exit): ").lower().strip()

                        if action == "s":
                            self.clear()
                            self.print_map()
                            for station in self.stations:
                                print(station.verbose())
                        if action == "d":
                            self.state = "DAY"
                    
