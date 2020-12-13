from .Game import Game

class TwoPGame(Game):

    # adds nPlayers = 2 to Game constructor
    def __init__(self):
        super().__init__()
        self.nPlayers = 2

    # returns turnNum of other player
    def otherPlayer(self, turnNum):
        return 3 - turnNum

    # determines winner in case of no legal moves
    def winsStalemate(self, gameState, turnNum):
        # player that goes second wins ties
        # makes the game "more interesting" (closer to balanced)
        return 2
