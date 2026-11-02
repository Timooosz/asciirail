import os
import random

from text import coord, printc

class Station:
    x = 0
    y = 0
    name = ""
    major = False
    display_name = "Unknown"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.major = random.choice((True, False))

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return self.display_name[0].lower() if not self.major else self.display_name[0].upper()

    def verbose(self):
        return f'{self.name} ({"Major" if self.major else "Minor"} {self.display_name}): {coord(self.x)}/{coord(self.y)}'
class Residential(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.display_name = "Residential"

class Commercial(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.display_name = "Commercial"

class Industrial(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.display_name = "Industrial"

class Medical(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.display_name = "Medical"

class Entertainment(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.display_name = "Entertainment"

class Park(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.display_name = "Park"

class TrainStation(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.display_name = "Train Station"


class Line:
    color = 0
    name = ""
    stations = []

def randomStation(x, y):
    return random.choices((Residential(x, y), Commercial(x, y), Industrial(x, y), Medical(x, y), Entertainment(x, y), Park(x, y), TrainStation(x, y)), (10, 5, 5, 3, 3, 3, 2))[0]

class Game:
    clear_cmd = ""
    board_size = 20
    stations = []
    running = True
    state = "MAP"
    lines = []

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
            x = min(max(station.x + random.randint(-5, 5), 0), self.board_size - 1)
            y = min(max(station.x + random.randint(-5, 5), 0), self.board_size - 1)
            found = True
            for existing in self.stations:
                if existing.x == x and existing.y == y: found = False
        return (x, y)

    def print_map(self, highlight_latest=False):
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
                        if highlight_latest:
                            printc(station, 1, 0)
                        else:
                            print(station, end="")
                        found = True
                if not found: print(" ", end="")
            print("")

    def new_station(self):
        position = self.new_position()
        station = randomStation(position[0], position[1])
        self.stations.append(station)
        self.clear()
        self.print_map(True)
        name = input(f'New Station{station.verbose()}. Enter a name for the Station: ')
        self.stations[-1].set_name(name)
        self.clear()
        self.print_map()

    def run(self):
        self.clear()

        while self.running:
            self.state = "MAP"
            while not self.state == "DAY":
                match self.state:

                    case "MAP":
                        self.new_station()
                        action = "?"
                        while action not in "blsx":
                            action = input("What do you want to do? (b: Begin Day, l: Line Editor, s: List Stations, x: Exit): ").lower().strip()

                        if action == "s":
                            self.clear()
                            self.print_map()
                            for station in self.stations:
                                print(station.verbose())
                        if action == "b":
                            self.state = "DAY"
                        if action == "l":
                            self.state = "LINE"
                        if action == "x":
                            self.running = False

                    case "LINE":
                        line_id = 0
                        
                        action = "?"
                        while action not in "bemnx" and not action.isdigit():
                            action = input("What do you want to do? (b: Begin Day, e: Edit Line, m: Show Map, n: New Line, x: Exit, Enter a number to select a line): ").lower().strip()

                        if action == "b":
                            self.state = "DAY"
                        if action == "m":
                            self.state = "MAP"
                        if action == "n":
                            pass
                        if action == "x":
                            self.running = False