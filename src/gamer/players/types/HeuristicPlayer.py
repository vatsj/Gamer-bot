from .Player import Player

# for simulated annealing to determine tempered move
import numpy as np
from scipy.special import softmax

# for cloning gameStates to choose next move
import copy

"""
Describes a player who moves to maximize some heuristic
Contains:
- heuristic fn h: (gameState, turnNum) --> Pr(win)
- temperature value temp (describes randomness in moves)

produced by HeuristicStrategist to optimize parameters to heuristic
"""

class HeuristicPlayer(Player):

    # Player + Heuristic info
    def __init__(self, game, turnNum, heuristic, temp):

        super().__init__(game, turnNum)

        # heuristic: gameState, turnNum --> Pr(win)
        self.HEURISTIC = heuristic
        self.TEMP = temp

        # modifiers for heuristic fn
        MODIFIERS_DEFAULT = {
            # memo-izing values of h
            "memo": False,
            # "Game Tree Augmented"
            # augmenting h with alpha-beta pruning
            "GTA": False,
        }

        self.modifiers = MODIFIERS_DEFAULT

        # probability of deletion from memoizer
        # unnecessary for arg-less heuristic per epoch
        self.PR_DELETION = 0
        # max depth for game tree search
        self.MAX_DEPTH = 2

    # makes tempered move based on heuristic and temp
    # chooses move by heuristic of resulting gameState
    # randomness introduced by temperature
    def makeMove(self, gameState):

        game = self.game
        turnNum = self.turnNum

        # computing info for next turn
        allMoves = game.getLegalMoves(game, gameState, turnNum)
        nMoves = game.nMoves(game, allMoves)
        nextTurnNum = game.nextTurn(turnNum)

        # copies gameState to test possible moves
        toy_gameState = copy.deepcopy(gameState)

        # determines heuristic scores of each available move
        move_hScores = []
        for move in allMoves:
            # resulting_gameState = copy.deepcopy(gameState)
            game.applyMove(game, toy_gameState, turnNum, move)
            curr_hScore = self.h_wrapper(toy_gameState, nextTurnNum)[turnNum - 1]
            game.undoMove(game, toy_gameState, turnNum, move)

            move_hScores.append(curr_hScore)

        hScores = np.array(move_hScores)

        # renders information about available moves
        if self.render:
            # first decimal point in Pr(win)
            hScores_render = []
            for hS in hScores:
                hScores_render.append(int(10*hS))

            print("\nheuristic scores:")
            print(hScores)
            print(game.render_gameBoard(game, gameState, hScores_render))

            # print("\nmodifiers:")
            # print(self.modifiers)

        # determines move probabilities from hScores
        # see link below for technical details:
        # https://en.wikipedia.org/wiki/Softmax_function#Reinforcement_learning
        if self.TEMP > 0:

            log_scores = np.log(hScores)

            # replacing the pr = 0 moves with some minimum log-probability
            MIN = -100
            log_scores = np.maximum(log_scores, MIN * np.ones(nMoves))
            # print(log_scores)

            softmax_scores = 1 / self.TEMP * log_scores
            move_probs = softmax(softmax_scores)

            # choosing random move given move_probs
            move_ind = np.random.choice(nMoves, p=move_probs)

        # t = 0 case reduces to argmax
        else:
            move_ind = np.argmax(hScores)

        move = allMoves[move_ind]
        return move

    # augments h with self.modifiers
    # modifiers gameState during method, should be unchanged after method runs
    """
    All heuristic methods are allowed to reversibly modify gameState
    cloning to create a toy_gameState happens outside h_wrapper, in makeMove
    """
    def h_wrapper(self, gameState, turnNum, modifiers = None):

        # sets default value for modifiers
        if not(modifiers):
            modifiers = self.modifiers

        memo = modifiers["memo"]
        GTA = modifiers["GTA"]

        game = self.game
        posn = game.encode_posn(game, gameState, turnNum)

        hVal = None

        # attempts to read from memoizer
        if self.modifiers["memo"]:

            # gets access to memoizer from observer strategist
            memoizer = self.observer.memoizer

            # if posn is memo-ized, reads value from memoizer
            if posn in memoizer:
                hVal = memoizer[posn]
                return hVal

            # otherwise attempts write to memoizer if memo = True
            elif memo:
                new_modifiers = copy.deepcopy(modifiers)
                new_modifiers["memo"] = False

                hVal = self.h_wrapper(gameState, turnNum, new_modifiers)
                memoizer[posn] = hVal
                return hVal

        # searches down game tree using multiplayer a-b pruning
        if GTA:
            # evaluates gameTree helper fn

            # modifiers are initialized, but without GTA
            # new_modifiers = copy.deepcopy(self.modifiers)

            # doesn't memoize new value after GTA
            new_modifiers = copy.deepcopy(modifiers)
            new_modifiers["GTA"] = False

            zeros = np.zeros(game.nPlayers)

            hVal = self.h_gameTree(gameState, turnNum, self.MAX_DEPTH, zeros, new_modifiers)
            # print(hVal)
            return hVal

        hVal = self.HEURISTIC(gameState, turnNum)
        return hVal

    # helper fn for alpha-beta pruning through gameTree
    def h_gameTree(self, gameState, turnNum, depth, min_winProbs, MODIFIERS):

        game = self.game

        # check if game has been won by any player
        winner = game.checkWin(game, gameState)
        if winner:
            # player `winner` wins with prob 1
            winProbs = np.zeros(game.nPlayers)
            winProbs[winner - 1] = 1
            return winProbs

        allMoves = game.getLegalMoves(game, gameState, turnNum)
        nMoves = game.nMoves(game, allMoves)
        nextTurnNum = game.nextTurn(turnNum)

        # checks if game is stalemated
        # if so, returns winning player
        if nMoves == 0:
            winner = game.winsStalemate(game, gameState, turnNum)

            # player `winner` wins with prob 1
            winProbs = np.zeros(game.nPlayers)
            winProbs[winner - 1] = 1
            return winProbs

        # if depth = 0, evaluate h at posn
        if depth == 0:
            hVal = self.h_wrapper(gameState, turnNum, MODIFIERS)
            return hVal

        # if depth > 0, check each branch of game tree

        zeros = np.zeros(game.nPlayers)
        ones = np.ones(game.nPlayers)

        # sort moves s.t. predicted best moves are tried first
        # improves likelihood of a-b pruning cutting down search space
        if depth > 1:

            # allMoves_list = []
            move_hScores = []
            for move in allMoves:

                # # adds move to allMoves_list
                # allMoves_list.append(move)

                # resulting_gameState = copy.deepcopy(gameState)
                game.applyMove(game, gameState, turnNum, move)
                curr_hScore = self.h_wrapper(gameState, nextTurnNum, MODIFIERS)[turnNum - 1]
                game.undoMove(game, gameState, turnNum, move)

                move_hScores.append(curr_hScore)

            # sorts moves in descending order (best moves first)
            hScore_order = np.argsort(-1 * np.array(move_hScores))
            # print(hScore_order)

            new_allMoves = [0 for i in range(nMoves)]
            for i in range(nMoves):
                ith_loc = hScore_order[i]
                new_allMoves[ith_loc] = allMoves[i]

            allMoves = new_allMoves
            # print(allMoves)

        # keeps track of winProbs for player turnNum's best move
        # instantiates to dummy values; to be overwritten
        optimal_winProbs = None
        optimal_tPwP = -1

        # iterates through moves, finds the best available
        for move in allMoves:

            # applies chosen move to resulting gamestate
            # resulting_gameState = copy.deepcopy(gameState)
            game.applyMove(game, gameState, turnNum, move)

            # recursively evaluates the position
            new_MWP = copy.deepcopy(min_winProbs)
            curr_winProbs = self.h_gameTree(gameState, nextTurnNum, depth - 1, new_MWP, MODIFIERS)

            # undoes move for this step (works recursively)
            game.undoMove(game, gameState, turnNum, move)

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
