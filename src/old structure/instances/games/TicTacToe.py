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
# print(T3)
T3.nPlayers = 2

# template definitions for Game object
me = T3

# board size
SIZE = 3

# returns value of the square given by coords
def getSquare(gameState, coords):
    i, j = coords
    return gameState[i][j]

# modifies value of the square given by coords
def getSquare(gameState, coords, val):
    i, j = coords
    gameState[i][j] = val

# returns the initial game state (upon starting a new game)
def startState(self):

    board = [[0 for j in range(SIZE)] for i in range(SIZE)]
    return board

# returns iterable of legal moves by given player in given gameState
def getLegalMoves(self, turnNum, gameState):

    moves = []
    for i in range(SIZE):
        for j in range(SIZE):
            move = (i, j)

            if getSquare(gameState, move) == 0:
                moves.append(move)

    return moves

# marks off square (i, j) with number given by turnNum
def applyMove(self, turnNum, gameState, move):

    setSquare(gameState, move, turnNum)

# checks if current player has any possible 3 in a row
def checkWin(self, turnNum, gameState):

    winning_sets = []

    # adding rows
    for i in range(SIZE):
        currSet = []

        for j in range(SIZE):
            currSet += (i, j)

        winning_sets += currSet

    # adding columns
    for j in range(SIZE):
        currSet = []

        for i in range(SIZE):
            currSet += (i, j)

        winning_sets += currSet

    # adding both diagonals
    d1_set = []
    d2_set = []
    for i in range(SIZE):
        d1_set += (i, i)
        d2_set += (i, (SIZE + 1) - i)

    winning_sets += d1_set
    winning_sets += d2_set

    # checks if turnNum player has any winning sets
    for ws in winning_sets:
        hasAll = True

        for square in ws:
            if (getSquare(gameState, square) != turnNum):
                hasAll  = False

        # if player has all of the winning set, they win
        if hasAll:
            return True

    return False

me.startState = startState
me.getLegalMoves = getLegalMoves
me.applyMove = applyMove
me.checkWin = checkWin
