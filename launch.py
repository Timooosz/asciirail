import os
from game import Game

clear_cmd = input("Enter the command that clears your terminal: ")

def clear():
    os.system(clear_cmd)

clear()

succeed = input("If the clear command was set correctly, this should be the only message. If so, press enter to proceed\n")

if succeed.lower().strip() != "":
    exit(-1)

board_size = input("Enter the board size (default: 20): ")
if not board_size.isdigit(): board_size = 20

game = Game(clear_cmd, int(board_size))

Game.run(game)

os.system("pause")