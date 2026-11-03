import random
from text import coord

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