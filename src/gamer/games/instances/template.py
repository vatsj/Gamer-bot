from .Game import Game

# Game object representing the game tic-tac-toe
_ = Game()
# print(T3)
_.nPlayers = 2

# template definitions for Game object
me = _

# returns the initial game state (upon starting a new game)
def startState(self):
    """instance-specific method"""
    pass

# returns iterable of legal moves by given player in given gameState
def getLegalMoves(self, gameState, turnNum):
    """instance-specific method"""
    pass

# applies "player makes move" to game state
# modifies gameState as an object
def applyMove(self, gameState, turnNum, move):
    pass

def checkWin(self, gameState):
    """instance-specific method"""
    pass

# determines winner in case of no legal moves
def winsStalemate(self, gameState, turnNum):
    """instance-specific method"""
    # returns default value of player 1
    return 1

me.startState = startState
me.getLegalMoves = getLegalMoves
me.applyMove = applyMove
me.checkWin = checkWin
me.winsStalemate = winsStalemate
me.render_gameState = render_gameState
