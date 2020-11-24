# import helper
# ih = helper.import_helper

import runpy
runpy.run_module("helper")
ih = import_helper

gameDir = "/src/types/Game.py"
playerDir = "/src/types/Player.py"

Game = ih(gameDir, "Game").Game
Player = ih(playerDir, "Player").Player

RandomPlayer = ih("/src/instances/players/Random.py", "Random").RandomPlayer
