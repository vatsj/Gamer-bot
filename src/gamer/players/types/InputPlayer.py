from .Player import Player

# inherits all but makeMove() fn from superclass
class InputPLayer(Player):

    # prompts user for move
    def makeMove(self, gameState):
        game = self.game
        allMoves = game.getLegalMoves(game, gameState, self.turnNum)

        print("\n Your turn - please enter a move.")
        print("All legal moves are listed below: ")
        print(allMoves)

        move = input()

        while not(move in allMoves):
            print("Invalid/illegal move! Please enter another move.")
            move = input()
