import importlib
import sys

# manually setting root dir
rootDir = "/home/jstav/Documents/Code/Projects/Gamer-bot"
gameDir = rootDir + "/src/types/Game.py"

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

# Game object representing the game tic-tac-toe
T3 = Game()
T3.nPlayers = 2

# template definitions for Game object
me = T3

# returns the initial game state (upon starting a new game)
def startState(self):
    """instance-specific method"""
    pass

# returns iterable of legal moves by given player in given gameState
def getLegalMoves(self, turnNum, gameState):
    """instance-specific method"""
    pass

# applies "player makes move" to game state, returns resulting game state
def applyMove(self, turnNum, gameState, move):
    pass

def checkWin(self, turnNum, gameState):
    """instance-specific method"""
    pass

me.startState = startState
me.getLegalMoves = getLegalMoves
me.applyMove = applyMove
me.checkWin = checkWin
