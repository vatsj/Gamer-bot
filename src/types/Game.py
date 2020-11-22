import queue

# abstract class representing a game playable between n players
class Game:

    # only initializes information about the game
    def __init__(self):
        nPlayers = null


    # plays an instance of the game, returns winner
    def play(self, players):

        # constructs turnOrder queue
        turnOrder = queue.Queue(nPlayers)
        for player in players:
            turnOrder.put(player)

        gameState = self.startState()

        while(True):
            # gets player taking current turn
            currTurn = turnOrder.get()
            turnOrder.put(currTurn)

            # player whose turn it is makes move
            move = currTurn.makeMove()
            gameState = self.applyMove(self, gameState, currTurn, move)

            if (self.checkWin(currturn, gameState)):
                return currTurn

    # returns the initial game state (upon starting a new game)
    def startState(self):
        """instance-specific method"""
        return null

    # returns iterable of legal moves by given player in given gameState
    def getLegalMoves(self, player, gameState):
        """instance-specific method"""
        return null

    # applies "player makes move" to game state, returns resulting game state
    def applyMove(self, player, gameState, move):
        """instance-specific method"""
        return null

    def checkWin(self, player, gameState):
        """instance-specific method"""
        return null
