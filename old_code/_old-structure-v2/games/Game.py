# testing import
print("importing Game")

# abstract class representing a game playable between n players
class Game:

    # imports inside class so instances will have access
    # import queue

    # only initializes information about the game
    def __init__(self):
        self.nPlayers = None


    # plays an instance of the game, returns winner
    def play(self, players):

        # constructs turnOrder queue
        # turnOrder = queue.Queue(self.nPlayers)
        # for player in players:
        #     turnOrder.put(player)

        gameState = self.startState()

        turnNum = 0
        while(True):

            # [1, 2, ... n] mod n
            turnNum = (turnNum % nPlayers) + 1

            # gets player taking current turn
            turnPlayer = players[turnNum]

            # player whose turn it is makes move
            move = turnPlayer.makeMove(gameState)
            if move in getLegalMoves(self, turnNum, gameState):
                self.applyMove(self, gameState, turnNum, move)
            else:
                raise Exception("Illegal move!")

            if (self.checkWin(turnNum, gameState)):
                return currTurn

    # returns the initial game state (upon starting a new game)
    def startState(self):
        """instance-specific method"""
        pass

    # returns iterable of legal moves by given player in given gameState
    def getLegalMoves(self, turnNum, gameState):
        """instance-specific method"""
        pass

    # applies "player makes move" to game state
    # modifies gameState as an object
    def applyMove(self, turnNum, gameState, move):
        pass

    def checkWin(self, turnNum, gameState):
        """instance-specific method"""
        pass
