from .HeuristicStrategist import HeuristicStrategist

# for win/loss dictionary
from collections import defaultdict

# uses a heuristic fn h: gameState --> Pr(win) to determine move
# trainingParams are precisely params of h
class MonteCarlo(HeuristicStrategist):



    # hParam: keeps track of games won/lost from the posn
    # hParams: (gameState, turnNum) --> [Pr(player i wins)]
    def getInitial_hParams(self):

        MC_dict = defaultdict(lambda: np.zeros(self.game.nPlayers))
        return MC_dict

    # returns a win frequency dict
    # identical to gI_hP
    def getInitial_hP_updater(self):

        MC_dict = defaultdict(lambda: np.zeros(self.game.nPlayers))
        return MC_dict

    # looks up past Pr(win) from MC_dict
    def h(self, gameState, turnNum, heuristicParams):

        MC_dict = heuristicParams

        winArr = MC_dict[(gameState, turnNum)]
        # adds laplace smoothing as a Beta(1, 1) (uniform) prior
        nWins =  winArr[turnNum - 1] + 1

        ones = np.ones(self.game.nPlayers)
        nTotal = ones.dot(winArr + ones)

        # monte-carlo probability of winning, with Laplace smoothing
        PrWin = nWins / nTotal
        return PrWin

    # updates hParams based on training games
    # update info is stored in hParam_updater obj
    def update_hParams(self, hParam_updater):

        DISCOUNT_FACTOR = 1/2
        MAX_SIZE = 10**6

        old_hParams = self.trainingParams

        old_keys = old_hParams.keys()
        new_keys = hParam_updater.keys()
        all_keys = old_keys + new_keys
        if len(all_keys) > MAX_SIZE:
            pruning = True
        else:
            pruning = False

        new_hParams = self.getInitial_hParams()

        # re-adds keys to new hParams
        for key in all_keys:
            winArr = DSICOUNT_FACTOR * old_keys[key] + new_keys[key]

            addKey = True

            # randomly choosing whether to record winArr
            if pruning:
                # weights consistent wins/losses above mixed
                significance = winArr.dot(winArr)

                # proportional to p(deletion) = 1/n^2
                # deletes significance = 1 keys with Pr = 1
                if (np.random.rand() < 1 / significance):
                    addKey = False

            if addKey:
                new_hParams[key] = winArr

    # overrides method to add movesList obj
    def getTrainerPlayer(self, turnNum):

        TP = super().getTrainerPlayer(turnNum)

        # attaches position list used by observation fns
        # eventually added to hParam_updater
        TP.positionSet = {}

    # canonical methods for TrainerPlayer observing move, result
    # can store information through access to player
    def observeTrainerMove(self, player, gameState, turnNum, move):

        # adds position to list
        key = (gameState, turnNum)
        player.positionSet += key

    # adds list to hParam_updater
    def observeTrainerResult(self, player, gameState, winner):

        toRecord = player.positionSet
        hParam_updater = player.hParam_updater

        # records that each position was won by wniner
        for key in toRecord:
            hParam_updater[key][winner - 1] += 1
