from .Strategist import Strategist

# uses a heuristic fn h: gameState --> Pr(win) to determine move
# trainingParams are precisely params of h
class HeuristicStrategist(Strategist):

    # heuristic function for Pr(win)
    # h: gameState, heuristicParams --> Pr(win)
    def h(self, gameState, heuristicParams):
        # """instance-specific method"""
        pass

    # produces an ObserverPlayer capable of playing games
    # the TrainerPlayer can (indirectly) update trainingParams
    def getTrainerPlayer(self):
        """instance-specific method"""
        pass

    # only a function of gameState, trainingParams
    def getOptimalMove(self, gameState, trainingParams):

        # evaluates "goodness" of move based on heuristic fn

    # optimizes for trainingParams given the inputted resource allotment
    def train(iters = 10**4):
        """instance-specific method"""
        pass
