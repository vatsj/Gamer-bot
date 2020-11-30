# agents that produce players to play a given game, training the agent
# can also produce their "optimal player" for the game, to compete
class Strategist:

    # stores the class defn to spawn ObserverPlayer-s
    # set/stored as a class property from main.py
    ObserverPlayer = None

    # takes in complete information about the finite game
    def __init__(self, game):

        # independent of turnNum
        # "knows how to play both sides of chess"
        self.game = game

        # trainingParams stores all trained information of the model
        self.trainingParams = None

        # flag for rendering info about move choice
        self.render = False

    # optimizes for trainingParams given the inputted resource allotment
    def train(self, iters):
        """instance-specific method"""
        pass

    # produces an ObserverPlayer capable of playing games
    # the TrainerPlayer can (indirectly) update trainingParams
    def getTrainerPlayer(self, turnNum):

        # ObserverPlayeris has strategist set to self (this class instance)
        TP = self.ObserverPlayer(self.game, turnNum, self)

        def makeMove(gameState):
            return self.getTrainerMove(TP, gameState, turnNum, self.trainingParams)

        TP.makeMove = makeMove
        return TP

    # produces moves for TrainerPlayers based on player and trainingParams
    def getTrainerMove(self, tp, gameState, turnNum, trainingParams):
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
    def getOptimalPlayer(self, turnNum):
        # only have access to ObserverPlayer class
        OP = self.ObserverPlayer(self.game, turnNum)

        def makeMove(gameState):
            return self.getOptimalMove(gameState, turnNum, self.trainingParams)

        OP.makeMove = makeMove
        return OP

    # produces optimal move for a given gameState
    # only a function of gameState, trainingParams
    def getOptimalMove(self, gameState, turnNum, trainingParams):
        """instance-specific method"""
        pass
