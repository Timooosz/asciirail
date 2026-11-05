import matplotlib.pyplot as plt

from game import Game

def draw_network(game: Game):
    lines = [line.stations for line in game.lines]

    print(lines)

    x_plots = []
    y_plots = []

    for line in lines:

        x_current = []
        y_current = []

        for station_name in line:
            station = [station for station in Game.stations if station.name == station_name][0]
            x_current.append(station.x)
            y_current.append(-station.y)

            plt.annotate(station.name, (station.x, -station.y))

        x_plots.append(x_current)
        y_plots.append(y_current)

    print(x_plots)
    print(y_plots)

    for i in range(len(x_plots)):
        plt.plot(x_plots[i], y_plots[i], marker='o')

    plt.show()