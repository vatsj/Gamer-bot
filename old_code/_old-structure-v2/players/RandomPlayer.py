from Player import Player

# inherits all but makeMove() fn from superclass
class RandomPlayer(Player):

    # to make random choices
    import random

    def makeMove(self, gameState):
        allMoves = self.game.getLegalMoves(turnNum, gameState)
        return random.choice(allMoves)
