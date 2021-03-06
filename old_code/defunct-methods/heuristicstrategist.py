# # augments h with self.modifiers
# def h_wrapper(self, gameState, turnNum, heuristicParams, modifiers = None):
#
#     # sets default value for modifiers
#     if not(modifiers):
#         modifiers = self.modifiers
#
#     memo = modifiers["memo"]
#     PR_DELETION = 1/10
#
#     GTA = modifiers["GTA"]
#     MAX_DEPTH = 2
#
#     game = self.game
#     posn = game.encode_posn(game, gameState, turnNum)
#
#     hVal = None
#
#     # attempts to read from memoizer
#     if self.modifiers["memo"]:
#
#         # if posn is memo-ized, reads value from memoizer
#         if posn in self.memoizer:
#             hVal = self.memoizer[posn]
#             return hVal
#
#         # otherwise attempts write to memoizer if memo = True
#         elif memo:
#             new_modifiers = copy.deepcopy(modifiers)
#             new_modifiers["memo"] = False
#
#             hVal = self.h_wrapper(gameState, turnNum, heuristicParams, new_modifiers)
#             self.memoizer[posn] = hVal
#             return hVal
#
#     # searches down game tree using multiplayer a-b pruning
#     if GTA:
#         # evaluates gameTree helper fn
#
#         # modifiers are initialized, but without GTA
#         # new_modifiers = copy.deepcopy(self.modifiers)
#
#         # doesn't memoize new value after GTA
#         new_modifiers = copy.deepcopy(modifiers)
#         new_modifiers["GTA"] = False
#
#         zeros = np.zeros(game.nPlayers)
#
#         hVal = self.h_gameTree(gameState, turnNum, heuristicParams, MAX_DEPTH, zeros, new_modifiers)
#         # print(hVal)
#         return hVal
#
#     hVal = self.h(gameState, turnNum, heuristicParams)
#     return hVal
#
# # helper fn for alpha-beta pruning through gameTree
# def h_gameTree(self, gameState, turnNum, hParams, depth, min_winProbs, MODIFIERS):
#
#     game = self.game
#
#     # check if game has been won by any player
#     winner = game.checkWin(game, gameState)
#     if winner:
#         # player `winner` wins with prob 1
#         winProbs = np.zeros(game.nPlayers)
#         winProbs[winner - 1] = 1
#         return winProbs
#
#     allMoves = game.getLegalMoves(game, gameState, turnNum)
#     nMoves = game.nMoves(game, allMoves)
#     nextTurnNum = game.nextTurn(turnNum)
#
#     # checks if game is stalemated
#     # if so, returns winning player
#     if nMoves == 0:
#         winner = game.winsStalemate(game, gameState, turnNum)
#
#         # player `winner` wins with prob 1
#         winProbs = np.zeros(game.nPlayers)
#         winProbs[winner - 1] = 1
#         return winProbs
#
#     # if depth = 0, evaluate h at posn
#     if depth == 0:
#         hVal = self.h_wrapper(gameState, turnNum, hParams, MODIFIERS)
#         return hVal
#
#     # if depth > 0, check each branch of game tree
#
#     toy_gameState = copy.deepcopy(gameState)
#
#     zeros = np.zeros(game.nPlayers)
#     ones = np.ones(game.nPlayers)
#
#     # sort moves s.t. predicted best moves are tried first
#     # improves likelihood of a-b pruning cutting down search space
#     if depth > 1:
#
#         # allMoves_list = []
#         move_hScores = []
#         for move in allMoves:
#
#             # # adds move to allMoves_list
#             # allMoves_list.append(move)
#
#             # resulting_gameState = copy.deepcopy(gameState)
#             game.applyMove(game, toy_gameState, turnNum, move)
#             curr_hScore = self.h_wrapper(toy_gameState, nextTurnNum, hParams, MODIFIERS)[turnNum - 1]
#             game.undoMove(game, toy_gameState, turnNum, move)
#
#             move_hScores.append(curr_hScore)
#
#         # sorts moves in descending order (best moves first)
#         hScore_order = np.argsort(-1 * np.array(move_hScores))
#         # print(hScore_order)
#
#         new_allMoves = [0 for i in range(nMoves)]
#         for i in range(nMoves):
#             ith_loc = hScore_order[i]
#             new_allMoves[ith_loc] = allMoves[i]
#
#         allMoves = new_allMoves
#         # print(allMoves)
#
#     # keeps track of winProbs for player turnNum's best move
#     # instantiates to dummy values; to be overwritten
#     optimal_winProbs = None
#     optimal_tPwP = -1
#
#     # iterates through moves, finds the best available
#     for move in allMoves:
#
#         # applies chosen move to resulting gamestate
#         # resulting_gameState = copy.deepcopy(gameState)
#         game.applyMove(game, toy_gameState, turnNum, move)
#
#         # recursively evaluates the position
#         new_MWP = copy.deepcopy(min_winProbs)
#         curr_winProbs = self.h_gameTree(toy_gameState, nextTurnNum, hParams, depth - 1, new_MWP, MODIFIERS)
#
#         # undoes move for this step (works recursively)
#         game.undoMove(game, toy_gameState, turnNum, move)
#
#         # checks if currMove is optimal
#         turnPlayer_winProb = curr_winProbs[turnNum - 1]
#         if turnPlayer_winProb > optimal_tPwP:
#             # updates optimal winProbs
#             optimal_winProbs = curr_winProbs
#             optimal_tPwP = turnPlayer_winProb
#
#         # alpha-beta pruning step
#
#         # updates min_winProbs based on current move
#         if turnPlayer_winProb > min_winProbs[turnNum - 1]:
#             min_winProbs[turnNum - 1] = turnPlayer_winProb
#
#         # prunes iff sum of min_winProbs > 1
#         # "some player can guarantee a better outcome via some other move"
#         if ones.dot(min_winProbs) > 1:
#
#             # current state will never be reached
#             # return 0 vec --> move will never be chosen
#             return zeros
#
#     # return winProbs for best move found
#     return optimal_winProbs
#
#
# # makeMove() helper fn
# # determines move based on simulated annealing with respect to heuristic fn
# # returns optimal move for player turnNum give gameState
# def makeTemperedMove(self, gameState, turnNum, hParams, temp, render = False):
#
#     game = self.game
#
#     # computing info for next turn
#     allMoves = game.getLegalMoves(game, gameState, turnNum)
#     nMoves = game.nMoves(game, allMoves)
#     nextTurnNum = game.nextTurn(turnNum)
#
#     # copies gameState to test possible moves
#     toy_gameState = copy.deepcopy(gameState)
#
#     # determines heuristic scores of each available move
#     move_hScores = []
#     for move in allMoves:
#         # resulting_gameState = copy.deepcopy(gameState)
#         game.applyMove(game, toy_gameState, turnNum, move)
#         curr_hScore = self.h_wrapper(toy_gameState, nextTurnNum, hParams)[turnNum - 1]
#         game.undoMove(game, toy_gameState, turnNum, move)
#
#         move_hScores.append(curr_hScore)
#
#     hScores = np.array(move_hScores)
#
#     # renders information about available moves
#     if render:
#         # first decimal point in Pr(win)
#         hScores_render = []
#         for hS in hScores:
#             hScores_render.append(int(10*hS))
#
#         print("\nheuristic scores:")
#         print(hScores)
#         print(game.render_gameBoard(game, gameState, hScores_render))
#
#         # print("\nmodifiers:")
#         # print(self.modifiers)
#
#     # determines move probabilities from hScores
#     # see link below for technical details:
#     # https://en.wikipedia.org/wiki/Softmax_function#Reinforcement_learning
#     if temp > 0:
#         # log_scores = []
#         # for elt in hScores:
#         #     currVal = None
#         #     if elt > 0:
#         #         currVal = np.log(elt)
#         #     else:
#         #         # minimum log-value of scores
#         #         MIN = -100
#         #         currVal = MIN
#         #
#         #     log_scores.append(currVal)
#
#         log_scores = np.log(hScores)
#
#         # replacing the pr = 0 moves with some minimum log-probability
#         MIN = -100
#         log_scores = np.maximum(log_scores, MIN * np.ones(nMoves))
#         # print(log_scores)
#
#         softmax_scores = 1/temp * log_scores
#         move_probs = softmax(softmax_scores)
#
#         # choosing random move given move_probs
#         move_ind = np.random.choice(nMoves, p=move_probs)
#
#     # t = 0 case reduces to argmax
#     else:
#         move_ind = np.argmax(hScores)
#
#     move = allMoves[move_ind]
#     return move
