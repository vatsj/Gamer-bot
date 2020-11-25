from .Player import Player

# to make random choices
import random

# inherits all but makeMove() fn from superclass
class RandomPlayer(Player):

    def makeMove(self, gameState):
        game = self.game
        allMoves = game.getLegalMoves(game, gameState, self.turnNum)
        return random.choice(allMoves)
