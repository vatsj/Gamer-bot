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
        print(game.render_gameBoard(game, gameState, allMoves_inds))

        move_ind = int(input())
        move = allMoves[move_ind]

        while not(move in allMoves):
            print("Invalid/illegal move! Please enter another move.")

            move_ind = int(input())
            move = allMoves[move_ind]

        return move
