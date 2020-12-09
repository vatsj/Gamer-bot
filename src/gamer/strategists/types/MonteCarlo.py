from .HeuristicStrategist import HeuristicStrategist

import numpy as np

import copy

# for win/loss dictionary
from collections import defaultdict

# uses a heuristic fn h: gameState --> Pr(win) to determine move
# trainingParams are precisely params of h
class MonteCarlo(HeuristicStrategist):

    # looks up past Pr(win) from MC_dict
    def h(self, gameState, turnNum, heuristicParams):

        game = self.game

        # check if game has been won by any player
        winner_ind = game.checkWin(game, gameState)
        if winner_ind:
            # player winner_ind wins with prob 1
            winProbs = np.zeros(game.nPlayers)
            winProbs[winner_ind - 1] = 1
            return winProbs

        # finds MC info based on encoded posn
        MC_dict = heuristicParams
        posn = game.encode_posn(game, gameState, turnNum)

        winArr = MC_dict[posn]
        # print(winArr)

        ones = np.ones(game.nPlayers)
        # adds laplace smoothing as a Beta(1, 1) (uniform) prior
        winArr_smoothed = winArr + ones

        # # monte-carlo probability of winning, with Laplace smoothing
        winProbs = winArr_smoothed / (ones.dot(winArr_smoothed))

        # print(winProbs)
        return winProbs

    # updates hParams based on training games
    # update info is stored in hParam_updater obj
    def update_hParams(self):

        DISCOUNT_FACTOR = 1/2

        # max size of MC_dict
        MAX_SIZE = 10**5
        # aggressive pruning
        # MAX_SIZE = 0

        # significance += 1 --> Pr(deletion) *= D_R
        DELETION_RATIO = 1/2

        old_hParams = self.trainingParams
        hParam_updater = self.hParam_updater

        old_keys = old_hParams.keys()
        new_keys = hParam_updater.keys()
        all_keys = {*old_keys, *new_keys}
        nKeys = len(all_keys)

        # if MC_dict gets too large, start pruning
        if nKeys > MAX_SIZE:
            pruning = True
        else:
            pruning = False
        print(nKeys, pruning)

        new_hParams = self.getInitial_hParams()

        # re-adds keys to new hParams
        for key in all_keys:
            # winArr magnitude is bounded due to discounting
            winArr = DISCOUNT_FACTOR * old_hParams[key] + hParam_updater[key]
            # print(winArr)

            addKey = True

            # randomly choosing whether to record winArr
            if pruning:
                # "magnitude of wins vector"
                # weights consistent wins/losses above mixed
                significance = np.power(winArr.dot(winArr), 1/2)

                # proportional to Pr(deletion) = (1/2)^n
                # "only deletes very low-confidence estimates"
                if (np.log(np.random.rand()) < significance * np.log(DELETION_RATIO)):
                    addKey = False

            if addKey:
                new_hParams[key] = winArr

        # updates hParams value
        self.trainingParams = new_hParams

    # hParam: keeps track of games won/lost from the posn
    # hParams: (gameState, turnNum) --> [Pr(player i wins)]
    def getInitial_hParams(self):

        MC_dict = defaultdict(lambda: np.zeros(self.game.nPlayers))
        return MC_dict

    # returns a win frequency dict
    # identical to gI_hP
    def getInitial_hP_updater(self):

        # MC_dict = defaultdict(lambda: np.zeros(self.game.nPlayers))
        # return MC_dict

        return self.getInitial_hParams()

    # hP_updater object given to TrainerPlayers
    # observer methods synthesize player hP_updater into strategist hP_updater
    def getPlayer_hP_updater(self):

        # list of encountered positions
        # will be labeled with result on observeResult()
        hP_updater = []

        return hP_updater

    # OBSERVER METHODS

    # canonical methods for TrainerPlayer observing move, result
    # can store information through access to player
    def observeMove(self, player, gameState, turnNum, move):

        # adds position to list
        game = self.game

        # records current gameState, NOT resulting one
        posn = game.encode_posn(game, gameState, turnNum)

        # # applies, records, then reverses move
        # toy_gameState = copy.deepcopy(gameState)
        #
        # game.applyMove(game, toy_gameState, turnNum, move)
        #
        # nextTurnNum = game.nextTurn(turnNum)
        # posn = game.encode_posn(game, toy_gameState, nextTurnNum)
        #
        # game.undoMove(game, toy_gameState, turnNum, move)

        player.hParam_updater.append(posn)

    # adds list to hParam_updater
    def observeResult(self, player, gameState, winner):

        # player.hParam updater is a list of encountered positions
        positionSet = player.hParam_updater

        # label each encountered position with this game's winner
        for posn in positionSet:
            posn_results = self.hParam_updater[posn]
            posn_results[winner - 1] += 1
