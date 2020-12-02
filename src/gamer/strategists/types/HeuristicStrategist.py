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

        # unpacks kwargs
        MODIFIERS_DEFAULT = {
            # memo-izing values of h
            "memo": False,
            # "Game Tree Augmented"
            # augmenting h with alpha-beta pruning
            "GTA": False,
        }

        self.modifiers = MODIFIERS_DEFAULT

        # # fills in missing kwargs with default values
        # for kw in kwargs_default.keys():
        #     if not (kw in kwargs.keys()):
        #         kwargs[kw] = kwargs_default[kw]
        #
        # # stores modifiers for computing h_wrapper in terms of h
        # self.modifiers = kwargs

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

    # augments h with self.modifiers
    def h_wrapper(self, gameState, turnNum, heuristicParams, modifiers = None):

        # sets default value for modifiers
        if not(modifiers):
            modifiers = self.modifiers

        memo = modifiers["memo"]
        PR_DELETION = 1/10

        GTA = modifiers["GTA"]
        MAX_DEPTH = 4

        game = self.game
        posn = game.encode_posn(game, gameState, turnNum)

        hVal = None

        # searches memoizer for encoded posn
        if memo:
            if posn in self.memoizer:

                # memoizer gets wiped every epoch, and hParams are constant per epoch
                # thus no need to delete mid-epoch

                # if (np.random.rand() < PR_DELETION):
                #
                #     new_modifiers = copy.deepcopy(modifiers)
                #     new_modifiers["memo"] = False
                #
                #     # compute and memoize new hval
                #     hVal = self.h_wrapper(self, gameState, turnNum, heuristicParams, new_modifiers)
                #     self.memoizer[posn] = hVal
                # else:
                #     # look up hval, DON'T re-memoize
                #     hVal = self.memoizer[posn]

                hVal = self.memoizer[posn]

            # computes and memoizes h value
            else:
                new_modifiers = copy.deepcopy(modifiers)
                new_modifiers["memo"] = False

                hVal = self.h_wrapper(gameState, turnNum, heuristicParams, new_modifiers)
                self.memoizer[posn] = hVal

            # returns regardless of memoization status
            return hVal

        # searches down game tree using multiplayer a-b pruning
        if GTA:
            # evaluates gameTree helper fn

            # modifiers are initialized, but without GTA
            new_modifiers = copy.deepcopy(self.modifiers)
            new_modifiers["GTA"] = False

            zeros = np.zeros(game.nPlayers)

            hVal = self.h_gameTree(self, gameState, turnNum, MAX_DEPTH, zeros, new_modifiers)
            return hVal

        hVal = self.h(gameState, turnNum, heuristicParams)
        return hVal

    # helper fn for alpha-beta pruning through gameTree
    def h_gameTree(self, gameState, turnNum, depth, min_winProbs, MODIFIERS):

        game = self.game

        # check if game has been won by any player
        winner_ind = game.checkWin(game, gameState)
        if winner_ind:
            # player winner_ind wins with prob 1
            winProbs = np.zeros(game.nPlayers)
            winProbs[winner_ind - 1] = 1
            return winProbs

        # if depth = 0, evaluate h at posn
        if depth == 0:
            hVal = h_wrapper(self, gameState, turnNum, heuristicParams, MODIFIERS)
            return hVal

        # if depth > 0, check each branch of game tree
        allMoves = game.getLegalMoves(game, gameState, turnNum)
        nextTurnNum = game.nextTurn(turnNum)

        zeros = np.zeros(game.nPlayers)
        ones = np.ones(game.nPlayers)

        # sort moves s.t. predicted best moves are tried first
        # improves likelihood of a-b pruning cutting down search space
        if depth > 1:

            move_hScores = []
            for move in allMoves:
                resulting_gameState = copy.deepcopy(gameState)
                game.applyMove(game, resulting_gameState, turnNum, move)
                curr_hScore = self.h_wrapper(resulting_gameState, nextTurnNum, hParams, MODIFIERS)[turnNum - 1]

                move_hScores.append(curr_hScore)

            # sorts moves in descending order (best moves first)
            hScore_order = np.argsort(-1 * np.array(move_hScores))

            new_allMoves = copy.deepCopy(zeros)
            for i in range(game.nPlayers):
                new_allMoves[hScore_order[i]] = allMoves[i]

            allMoves = new_allMoves

        # keeps track of winProbs for player turnNum's best move
        optimal_winProbs = zeros
        optimal_tPwP = optimal_winProbs[turnNum - 1]

        # iterates through moves, finds the best available
        for move in allMoves:

            # applies chosen move to resulting gamestate
            resulting_gameState = copy.deepcopy(gameState)
            game.applyMove(game, resulting_gameState, turnNum, move)

            # recursively evaluates the position
            new_MWP = copy.deepcopy(min_winProbs)
            curr_winProbs = self.h_gameTree(self, resulting_gameState, nextTurnNum, depth - 1, new_MWP, MODIFIERS)

            # checks if currMove is optimal
            turnPlayer_winProb = curr_winProbs[turnNum - 1]
            if turnPlayer_winProb > optimal_tPwP:
                # updates optimal winProbs
                optimal_winProbs = curr_winProbs
                optimal_tPwP = turnPlayer_winProb

            # alpha-beta pruning step

            # updates min_winProbs based on current move
            if turnPlayer_winProb > min_winProbs[turnNum - 1]:
                min_winProbs[turnNum - 1] = turnPlayer_winProb

            # prunes iff sum of min_winProbs > 1
            # "some player can guarantee a better outcome via some other move"
            if ones.dot(min_winProbs) > 1:

                # current state will never be reached
                # return 0 vec --> move will never be chosen
                return zeros

        # return winProbs for best move found
        return optimal_winProbs


    # makeMove() helper fn
    # determines move based on simulated annealing with respect to heuristic fn
    # returns optimal move for player turnNum give gameState
    def makeTemperedMove(self, gameState, turnNum, hParams, temp, render = False):

        game = self.game
        allMoves = game.getLegalMoves(game, gameState, turnNum)
        nextTurnNum = game.nextTurn(turnNum)

        # determines heuristic scores of each available move
        move_hScores = []
        for move in allMoves:
            resulting_gameState = copy.deepcopy(gameState)
            game.applyMove(game, resulting_gameState, turnNum, move)
            curr_hScore = self.h_wrapper(resulting_gameState, nextTurnNum, hParams)[turnNum - 1]

            move_hScores.append(curr_hScore)

        hScores = np.array(move_hScores)

        # renders information about available moves
        if render:
            # first decimal point in Pr(win)
            hScores_render = []
            for hS in hScores:
                hScores_render.append(int(10*hS))

            print("\nheuristic scores:")
            print(hScores)
            print(game.render_gameBoard(game, gameState, hScores_render))

        # determines move probabilities from hScores
        # see link below for technical details:
        # https://en.wikipedia.org/wiki/Softmax_function#Reinforcement_learning
        if temp > 0:
            softmax_scores = 1/temp * np.log(hScores)
            move_probs = softmax(softmax_scores)

            # choosing random move given move_probs
            move_ind = np.random.choice(len(allMoves), p=move_probs)

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

        # pings n times during training to keep tabs on progress
        TRAINING_PINGS = 50
        TPN = 0

        for epoch in range(nEpochs):

            # accounts for memoizer
            if (self.modifiers["memo"]):
                self.memoizer = {}

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

            self.update_hParams(hParam_updater)

            # pings training progress as the bot trains
            if (epoch / nEpochs > TPN / TRAINING_PINGS):
                # updates TPN
                TPN += 1

                print("Training progress: \t", epoch / nEpochs)
                print("sample game below: \n")

                players = [self.getOptimalPlayer(i + 1) for i in range(game.nPlayers)]
                game.play(players, render=True)

    # updates hParams based on training games
    # update info is stored in hParam_updater obj
    def update_hParams(self, hParam_updater):
        """instance-specific method"""
        pass

    # produces moves for TrainerPlayers based on player and trainingParams
    def getTrainerMove(self, tp, gameState, turnNum, trainingParams):

        # tempered move with temp given by player
        temp = tp.temp
        hParams = trainingParams

        move = self.makeTemperedMove(gameState, turnNum, hParams, temp)
        return move

    # produces optimal move for a given gameState
    # only a function of gameState, trainingParams
    def getOptimalMove(self, gameState, turnNum, trainingParams):

        # tempered move with temp = 0
        move = self.makeTemperedMove(gameState, turnNum, trainingParams, 0, self.render)
        return move
