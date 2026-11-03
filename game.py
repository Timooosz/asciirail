import os
import random

from text import coord, printc

from station import Station, Residential, Commercial, Industrial, Medical, Entertainment, Park, TrainStation

class Line:
    color = 0
    name = ""

    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.stations = []

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
                for i, station in enumerate(self.stations):
                    if station.x == x and station.y == y:
                        if highlight_latest and i == len(self.stations) - 1:
                            printc(station, 1, 0)
                        else:
                            print(station, end="")
                        found = True
                if not found: print(" ", end="")
            print("")

    def print_map_line(self, index):
        for y in range(self.board_size):
            for x in range(self.board_size):
                found = False
                for i, station in enumerate(self.stations):
                    if station.x == x and station.y == y:
                        if station.name in self.lines[index].stations:
                            printc(self.lines[index].stations.index(station.name), self.lines[index].color, 0)
                        else:
                            print("x", end=" ")
                        found = True
                if not found: print(" ", end=" ")
            print("")

    def new_station(self):
        position = self.new_position()
        station = randomStation(position[0], position[1])
        self.stations.append(station)
        self.clear()
        self.print_map(True)
        name = input(f'New Station{station.verbose()}. Enter a name for the station: ')
        self.stations[-1].set_name(name)
        self.clear()
        self.print_map()

    def print_line(self, index):
        if len(self.lines) <= index:
            print("Line does not exist")
            return
        printc(self.lines[index].name, 7, self.lines[index].color)
        print("")
        if len(self.lines[index].stations) == 0:
            print("No stations added to line")
            return
        for station in self.lines[index].stations:
            printc(" I\n", self.lines[index].color, 0)
            print(" O ", end="")
            print(station, end="")
            transfers = []
            for i, line in enumerate(self.lines):
                if i == index: continue
                if station in line.stations: transfers.append(line)
            if len(transfers) > 0:
                print(" -> ", end="")
                for transfer in transfers:
                    printc(transfer.name, 7, transfer.color)
                
            print("")
        print("")

    def run(self):
        self.clear()

        self.state = "MAP"
        line_id = 0
        for _ in range(2):
            self.new_station()

        while self.running:
            self.state = "MAP"
            line_id = 0
            self.new_station()
            while not self.state == "DAY":

                match self.state:

                    case "MAP":
                        action = "?"
                        while action not in "blsx":
                            action = input("What do you want to do? (b: Begin Day, l: Line Editor, s: List Stations, x: Exit): ").lower().strip()

                        if action == "s":
                            self.clear()
                            self.print_map()
                            for station in self.stations:
                                print(station.verbose(), end="")
                                for line in self.lines:
                                    if station.name in line.stations:
                                        printc(line.name, 7, line.color)
                                print("")
                        if action == "b":
                            self.state = "DAY"
                        if action == "l":
                            self.state = "LINE"
                            self.clear()
                        if action == "x":
                            self.running = False

                    case "LINE":

                        if len(self.lines) == 0:
                            print("You do not have any lines")
                        else:
                            print("Your lines:", end="")
                            for line in self.lines:
                                printc(line.name, 7, line.color)
                                print(" ", end="")
                            print("\n==========")
                                
                            if len(self.lines) > 0:
                                self.print_line(line_id)
                                self.print_map_line(line_id)

                        
                        action = "?"
                        while action not in "abdmnrx" and not action.isdigit():
                            action = input("What do you want to do? (a: Add Station, b: Begin Day, d: Delete Line, m: Show Map, n: New Line, r: Remove Station, x: Exit, Enter a number to select a line): ").lower().strip()

                        if action == "a":
                            index = int(input("At index: "))
                            if index > len(self.lines[line_id].stations):
                                print("Invalid index")
                                self.clear()
                                continue
                            name = input("Name of the station to add: ")
                            if True not in [station.name == name for station in self.stations]:
                                print("Station does not exist")
                                self.clear()
                                continue
                            
                            self.lines[line_id].stations.insert(index, name)
                            self.clear()
                            
                        if action == "b":
                            self.state = "DAY"
                        if action == "d":
                            if len(self.lines) > 0:
                                self.lines.pop(line_id)
                        if action == "m":
                            self.state = "MAP"
                            self.clear()
                            self.print_map()
                        if action == "n":
                            line_name = input("Name of the line: ")
                            for i in range(7):
                                printc(i, 7, i)
                                print(" ", end="")
                            line_color = input(" Which color?: ")
                            self.lines.append(Line(int(line_color), line_name))
                            self.clear()
                        if action == "r":
                            station_name = input("Name of the station: ")
                            if station_name in self.lines[line_id].stations:
                                self.lines[line_id].remove(station_name)
                        if action == "x":
                            self.running = False
                        if action.isdigit():
                            if int(action) < len(self.lines):
                                line_id = int(action)
                                self.clear()
                            else:
                                print("Line does not exist")
                                self.clear()