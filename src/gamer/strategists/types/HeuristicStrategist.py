from .Strategist import Strategist

# for simulated annealing to determine tempered move
import numpy as np
from scipy.special import softmax

# for cloning gameStates to choose next move
import copy

# uses a heuristic fn h: gameState --> Pr(win) to determine move
# trainingParams are precisely params of h
class HeuristicStrategist(Strategist):

    # takes in complete information about the finite game
    def __init__(self, game):

        super().__init__(game)

        # trainingParams = heuristicParams
        self.trainingParams = self.getInitial_hParams()

        # initializing paramater-less heuristic fn
        # to be passed to TrainerPlayer-s
        # re-evaluates each time based on current hParams
        def heuristic(gameState, turnNum):
            return self.h(gameState, turnNum, self.trainingParams)

        self.heuristic = heuristic

        # unpacks kwargs
        MODIFIERS_DEFAULT = {
            # memo-izing values of h
            "memo": False,
            # "Game Tree Augmented"
            # augmenting h with alpha-beta pruning
            "GTA": False,
        }

        self.modifiers = MODIFIERS_DEFAULT

    # returns an initial value for hParams
    def getInitial_hParams(self):
        """instance-specific method"""
        pass

    # returns an initial value for hP_updater
    def getInitial_hP_updater(self):
        """instance-specific method"""
        pass

    # hP_updater object given to TrainerPlayers
    # observer methods synthesize player hP_updater into strategist hP_updater
    def getPlayer_hP_updater(self):
        """instance-specific method"""
        pass

    # updates hParams based on training games
    # update info is stored in hParam_updater obj
    def update_hParams(self):
        """instance-specific method"""
        pass

    # heuristic function for Pr(win)
    # h: gameState, heuristicParams --> [Pr(player i wins)]
    def h(self, gameState, turnNum, heuristicParams):
        """instance-specific method"""
        pass

    # optimizes for trainingParams given the inputted resource allotment
    def train(self, iters = 10**5):
        # can probably implement this in terms of a heuristic updater method?
        game = self.game

        # breaks down training into epochs
        EPOCH_SIZE = int(np.power(iters, 2/3))
        nEpochs = iters // EPOCH_SIZE

        # want 1-0 to be a substantial part of training time
        # google the theory behind this later?
        INITIAL_TEMP = 2

        # pings n times during training to keep tabs on progress
        TRAINING_PINGS = 50
        TPN = 0

        for epoch in range(nEpochs):

            # accounts for memoizer
            if (self.modifiers["memo"]):
                self.memoizer = {}

            # initializing temp for this epoch's players
            # heuristic = lambda gameState, turnNum: self.h(gameState, turnNum, self.trainingParams)
            temp = INITIAL_TEMP * (1 - epoch / nEpochs)

            # hParam_updater is a property of the strategist
            self.hParam_updater = self.getInitial_hP_updater()

            for game_count in range(EPOCH_SIZE):

                # plays a training game against itself by default
                players = []
                for i in range(game.nPlayers):
                    # constructs TrainerPlayer as HeuristicPlayer
                    currPlayer = self.getTrainerPlayer(i + 1, self.heuristic, temp)

                    # specific properties of TrainerPlayer-s
                    # currPlayer.temp = temp
                    # currPlayer.hParam_updater = hParam_updater

                    players.append(currPlayer)

                # plays game against itelf
                game.play(players, training=True)

            # synthesizes hParam_updater with hParams
            self.update_hParams()

            # pings training progress as the bot trains
            if (epoch / nEpochs > TPN / TRAINING_PINGS):
                # updates TPN
                TPN += 1

                print("Training progress: \t", epoch / nEpochs)
                print("sample game below: \n")

                # optimal players with rendering flag on
                players = []
                for i in range(game.nPlayers):
                    currPlayer = self.getOptimalPlayer(i + 1)
                    # currPlayer.render = True

                    players.append(currPlayer)

                game.play(players, render=True)

    # produces a HeuristicPlayer capable of playing games
    def getTrainerPlayer(self, turnNum, heuristic, temp):

        TP = self.players.types.HeuristicPlayer(self.game, turnNum, self.heuristic, temp)

        # configuring trainer player properties
        TP.setObserver(self)
        TP.modifiers = self.modifiers
        TP.hParam_updater = self.getPlayer_hP_updater()

        return TP

    # produces the player using the strategist's "optimal strategy"
    def getOptimalPlayer(self, turnNum):

        # optimal player has temp = 0
        temp = 0

        OP = self.players.types.HeuristicPlayer(self.game, turnNum, self.heuristic, temp)

        # turns memoizer off; only used for training
        modifiers = self.modifiers
        modifiers["memo"] = False
        OP.modifiers = modifiers

        return OP

    # OBSERVER METHODS

    # canonical methods for TrainerPlayer observing move, result
    # can store information through access to player
    def observeMove(self, player, gameState, turnNum, move):
        """instance-specific method"""
        pass

    def observeResult(self, player, gameState, winner):
        """instance-specific method"""
        pass
