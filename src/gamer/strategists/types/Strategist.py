# agents that produce players to play a given game, training the agent
# can also produce their "optimal player" for the game, to compete
class Strategist:

    # takes in complete information about the finite game
    def __init__(self, game, turnNum)

        self.game = game
        self.turnNum = turnNum

        # trainingParams stores all trained information of the model
        self.trainingParams = None

    # optimizes for trainingParams given the inputted resource allotment
    def train(iters = 10**4):
        """instance-specific method"""
        pass

    # produces an ObserverPlayer capable of playing games
    # the TrainerPlayer can (indirectly) update trainingParams
    def getTrainerPlayer(self):

        TP = Player(self.game, self.turnNum)

        def makeMove(TP_self, gameState):
            return getTrainerMove(self, TP_self, gameState, self.trainingParams)

        TP.makeMove = makeMove
        return TP

    # produces moves for TrainerPlayers based on player and trainingParams
    def getTrainerMove(self, tp, gameState, trainingParams):
        """instance-specific method"""
        pass

    # canonical methods for TrainerPlayer observing move, result
    # can store information through access to player
    def observeTrainerMove(self, player, gameState, turnNum, move):
        """instance-specific method"""
        pass

    def observeTrainerResult(self, player, gameState, winner):
        """instance-specific method"""
        pass

    # produces the player using the strategist's "optimal strategy"
    # plays in terms of getOptimalMove
    def getOptimalPlayer(self):
        # do we have access to Player class?
        OP = Player(self.game, self.turnNum)

        def makeMove(OP_self, gameState):
            return getOptimalMove(self, gameState, self.trainingParams)

        OP.makeMove = makeMove
        return OP

    # produces optimal move for a given gameState
    # only a function of gameState, trainingParams
    def getOptimalMove(self, gameState, trainingParams):
        """instance-specific method"""
        pass
