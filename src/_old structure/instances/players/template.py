import importlib
import sys

# manually setting root dir
rootDir = "/home/jstav/Documents/Code/Projects/Gamer-bot"
gameDir = rootDir + "/src/types/Game.py"
playerDir = rootDir + "/src/types/Player.py"

def import_helper(path, name):
    MODULE_PATH = path
    MODULE_NAME = name

    # imports path as "module"
    spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module

Game = import_helper(gameDir, "Game").Game
Player = import_helper(playerDir, "Player").Player

# inherits all but makeMove() fn from superclass
class RandomPlayer(Player):

    # to make random choices
    import random

    def makeMove(self, gameState):
        allMoves = self.game.getLegalMoves(turnNum, gameState)
        return random.choice(allMoves)
