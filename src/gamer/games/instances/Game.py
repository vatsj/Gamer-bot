# abstract class representing a game playable between n players
class Game:

    # only initializes information about the game
    def __init__(self):
        self.nPlayers = None


    # plays an instance of the game, returns winner
    # kwargs: render, training
    def play(self, players, **kwargs):

        # unpacks kwargs
        kwargs_default = {
            "render": False,
            "training": False,
        }

        # fills in missing kwargs with default values
        for kw in kwargs_default.keys():
            if not (kw in kwargs.keys()):
                kwargs[kw] = kwargs_default[kw]

        # testing
        render = kwargs["render"]
        training = kwargs["training"]


        gameState = self.startState(self)

        turnNum = 0
        winner = None
        while not(winner):

            # [1, 2, ... n] mod n
            turnNum = self.nextTurn(turnNum)

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

            # else, plays next move
            else:

                # player whose turn it is makes move
                # print(turnPlayer)
                move = turnPlayer.makeMove(gameState)
                # move = turnPlayer.makeMove(turnPlayer, gameState)

                # checks if move is legal
                if not(move in self.getLegalMoves(self, gameState, turnNum)):
                    raise Exception("Illegal move!")

                # all ObserverPlayers observe move as it is made
                if training:
                    # each ObserverPlayer observes move
                    for op in players:
                        if hasattr(op, "strategist"):
                            op.strategist.observeTrainerMove(op, gameState, turnNum, move)

                # applies move to gameState
                # MODIFIES GAMESTATE IN PLACE
                self.applyMove(self, gameState, turnNum, move)

                if render:
                    print("Player ", turnNum, "makes the following move: \t", move)

                winner = self.checkWin(self, gameState)

                if winner:
                    if render:
                        print("The resulting position is won by player ", turnNum)

        # game ended; display and return winner
        if render:
            print("\nPlayer ", winner, "has won!")
            print("The winning board state is below: \n")
            print(self.render_gameState(self, gameState))

        # all ObserverPlayers observe game being won
        if training:
            # each ObserverPlayer observes move
            for op in players:
                if hasattr(op, "strategist"):
                    op.strategist.observeTrainerResult(op, gameState, winner)

        return winner

    # vars in order of scale
    # gameState, turnNum, move

    # returns the initial game state (upon starting a new game)
    def startState(self):
        """instance-specific method"""
        pass

    def nextTurn(self, turnNum):
        return (turnNum % self.nPlayers) + 1

    # returns iterable of legal moves by given player in given gameState
    def getLegalMoves(self, gameState, turnNum):
        """instance-specific method"""
        pass

    # applies "player makes move" to game state
    # modifies gameState in place
    def applyMove(self, gameState, turnNum, move):
        pass

    # checks if any player has won
    # returns False if not
    def checkWin(self, gameState):
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

    # encodes gameState, turnNum for dictionary storage
    # returns immutable object (dictionary-friendly)
    def encode_posn(self, gameState, turnNum):
        """instance-specific method"""
        pass
