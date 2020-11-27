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
    def __init__(self, game, turnNum, **kwargs):

        self.game = game
        self.turnNum = turnNum

        # trainingParams = heuristicParams
        self.trainingParams = self.getInitial_hParams()

        # unpacks kwargs
        kwargs_default = {
            # memo-izing values of h
            "memo": False,
            # augmenting h with alpha-beta pruning
            "GTA": False,
        }

        # fills in missing kwargs with default values
        for kw in kwargs_default.keys():
            if not (kw in kwargs.keys()):
                kwargs[kw] = kwargs_default[kw]

        self.kwargs = kwargs

    # returns an initial value for hParams
    def getInitial_hParams(self):
        """instance-specific method"""
        pass

    # returns an initial value for hP_updater
    def getInitial_hP_updater(self):
        """instance-specific method"""
        pass

    # heuristic function for Pr(win)
    # h: gameState, heuristicParams --> [Pr(player i wins)]
    def h(self, gameState, turnNum, heuristicParams):
        """instance-specific method"""
        pass

    def h_wapper(self, gameState, turnNum, heuristicParams):

        # handle augmentations from kwargs
        return h(self, gameState, turnNum, heuristicParams)

    # makeMove() helper fn
    # determines move based on simulated annealing with respect to heuristic fn
    # returns optimal move for player turnNum give gameState
    def makeTemperedMove(gameState, turnNum, hParams, temp):

        game = self.game
        allMoves = game.getLegalMoves(game, gameState, turnNum)
        nextTurnNum = game.nextTurn(game)

        # determines heuristic scores of each available move
        move_hScores = []
        for move in allMoves:
            resulting_gameState = copy.copy(gameState)
            game.applyMove(game, resulting_gameState, turnNum, move)
            curr_hScore = self.h_wrapper(self, resulting_gameState, nextTurnNum, hP)[turnNum - 1]

            move_hScores.append(curr_hScore)

        hScores = np.array(move_hScores)

        # determines move probabilities from hScores
        # see link below for technical details:
        # https://en.wikipedia.org/wiki/Softmax_function#Reinforcement_learning
        if temp > 0:
            softmax_scores = 1/temp * np.log(hScores)
            move_probs = softmax(softmax_scores)

            # choosing random move given move_probs
            move = np.random.choice(allMoves, p=move_probs)

        # t = 0 case reduces to argmax
        else:
            move_ind = np.argmax(hScores)
            move = allMoves[move_ind]

        return move

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

        for epoch in range(nEpochs):
            temp = INITIAL_TEMP * (1 - epoch / nEpochs)
            hParam_updater = self.getInitial_hP_updater()

            for game_count in range(EPOCH_SIZE):

                # plays a training game against itself by default
                players = []
                for i in range(game.nPlayers):
                    currPlayer = self.getTrainerPlayer(i + 1)

                    # specific properties of TrainerPlayer-s
                    currPlayer.temp = temp
                    currPlayer.hParam_updater = hParam_updater

                    players.append(currPlayer)

                # plays game against itelf
                game.play(players, training=True)

            self.update_hParams(self, hParam_updater)

    # updates hParams based on training games
    # update info is stored in hParam_updater obj
    def update_hParams(self, hParam_updater):
        """instance-specific method"""
        pass

    # produces moves for TrainerPlayers based on player and trainingParams
    def getTrainerMove(self, tp, gameState, trainingParams):

        # tempered move with temp given by player
        temp = tp.temp
        hParams = trainingParams

        move = self.makeTemperedMove(gameState, self.turnNum, hParams, temp)
        return move

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

        # tempered move with temp = 0
        move = self.makeTemperedMove(gameState, self.turnNum, trainingParams, 0)
        return move
