from .Player import Player

# adds new observer methods to superclass
class ObserverPlayer(Player):

    # Player + Strategist
    def __init__(self, game, turnNum, strategist):

        super().__init__(game, turnNum)

        # adds parent strategist as object property
        self.strategist = strategist

    def makeMove(self, gameState):
        """instance-specific method"""
        pass


    def observeMove(self, turnNum, gameState, move):
        """instance-specific method"""
        pass

    def observeResult(self, gameState, winner):
        """instance-specific method"""
        pass
