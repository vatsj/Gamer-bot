# abstract class representing a game playable between n players
class Game:

    # only initializes information about the game
    def __init__(self):
        self.nPlayers = None


    # plays an instance of the game, returns winner
    def play(self, players, render = False):

        # constructs turnOrder queue
        # turnOrder = queue.Queue(self.nPlayers)
        # for player in players:
        #     turnOrder.put(player)

        gameState = self.startState(self)

        turnNum = 0
        while(True):

            # [1, 2, ... n] mod n
            turnNum = (turnNum % self.nPlayers) + 1

            # gets player taking current turn
            turnPlayer = players[turnNum - 1]

            if render:
                print("\n"*10)
                print("Current board: \n")
                print(self.render_gameState(self, gameState))

                print("\n Player ", turnNum, " to move. \n")

            # checks for stalemate
            # if so, determines winner
            if len(self.getLegalMoves(self, gameState, turnNum)) == 0:
                winner = self.winsStalemate(self, gameState, turnNum)

                if render:
                    print("Player ", turnNum, " has no valid moves!")
                    print("Thus, player ", winner, " is declared the winner.")

                return winner

            # player whose turn it is makes move
            move = turnPlayer.makeMove(gameState)
            if move in self.getLegalMoves(self, gameState, turnNum):
                self.applyMove(self, gameState, turnNum, move)
            else:
                raise Exception("Illegal move!")

            if render:
                print("Player ", turnNum, "makes the following move: \t", move)

            if (self.checkWin(self, gameState, turnNum)):
                winner = turnNum

                if render:
                    print("Player ", winner, "has won!")
                    print("The winning board state is below: \n")
                    print(self.render_gameState(self, gameState))

                return winner

    # vars in order of scale
    # gameState, turnNum, move

    # returns the initial game state (upon starting a new game)
    def startState(self):
        """instance-specific method"""
        pass

    # returns iterable of legal moves by given player in given gameState
    def getLegalMoves(self, gameState, turnNum):
        """instance-specific method"""
        pass

    # applies "player makes move" to game state
    # modifies gameState as an object
    def applyMove(self, gameState, turnNum, move):
        pass

    # checks if the player that just moved won the game
    def checkWin(self, gameState, turnNum):
        """instance-specific method"""
        pass

    # determines winner in case of no legal moves
    def winsStalemate(self, gameState, turnNum):
        """instance-specific method"""
        # returns default value of player 1
        return 1


    # graphics-rendering fns

    # renders the game board
    def render_gameState(self, gameState):
        """instance-specific method"""
        pass