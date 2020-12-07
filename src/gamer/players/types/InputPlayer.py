from .Player import Player

# inherits all but makeMove() fn from superclass
class InputPlayer(Player):

    # prompts user for move
    def makeMove(self, gameState):
        game = self.game
        allMoves = game.getLegalMoves(game, gameState, self.turnNum)
        allMoves_inds = [i for i in range(len(allMoves))]

        # indexes moves, so human can input move index
        # count = 0
        # moveDict = {}
        # for move in allMoves:
        #     count += 1
        #     moveDict[count] = move

        print("\n Your turn - please enter a move.")
        print("All legal moves are listed below: ")

        # uses render_gameBoard if available, otherwise prints move dict
        allMoves_rendered = game.render_gameBoard(game, gameState, allMoves_inds)
        if allMoves_rendered:
            print(allMoves_rendered)
        else:
            for ind in allMoves_inds:
                print(ind, ": \t", allMoves[ind])

        move_ind = int(input())
        move = allMoves[move_ind]

        while not(move in allMoves):
            print("Invalid/illegal move! Please enter another move.")

            move_ind = int(input())
            move = allMoves[move_ind]

        return move
