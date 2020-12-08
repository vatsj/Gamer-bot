# abstract class representing a player of a given game
class Player:

    # player i in a given game
    def __init__(self, game, turnNum):

        self.game = game
        self.turnNum = turnNum

        # flag for rendering move info
        self.render = False

    # sets given strategist as observer
    def setObserver(self, strategist):
        # takes in a strategist as an observer object
        self.observer = strategist

    # returns the move to be made
    # must be an element of self.game.getLegalMoves()
    def makeMove(self, gameState):
        """instance-specific method"""
        pass
