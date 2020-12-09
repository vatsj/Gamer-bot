# agents that produce players to play a given game, training the agent
# can also produce their "optimal player" for the game, to compete
class Strategist:

    # stores the class defn to spawn Player objects
    # set/stored as a class property from main.py
    players = None

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

    """
    methods to generate players
    bot trains by generating and playing TrainerPlayers against themselves
    """

    # produces an ObserverPlayer capable of playing games
    def getTrainerPlayer(self, turnNum):
        """instance-specific method"""
        pass

    # produces the player using the strategist's "optimal strategy"
    def getOptimalPlayer(self, turnNum):
        """instance-specific method"""
        pass

    # OBSERVER METHODS

    # canonical methods for TrainerPlayer observing move, result
    # can store information through access to player
    def observeMove(self, player, gameState, turnNum, move):
        """instance-specific method"""
        pass

    def observeResult(self, player, gameState, winner):
        """instance-specific method"""
        pass
