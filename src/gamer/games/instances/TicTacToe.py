from .Game import Game

# Game object representing the game tic-tac-toe
T3 = Game()
# print(T3)
T3.nPlayers = 2

# template definitions for Game object
me = T3

# board size
SIZE = 3

# returns value of the square given by coords
def getSquare(gameState, coords):
    i, j = coords
    return gameState[i][j]

# modifies value of the square given by coords
def setSquare(gameState, coords, val):
    i, j = coords
    # print(gameState)
    gameState[i][j] = val

# returns the initial game state (upon starting a new game)
def startState(self):

    board = [[0 for j in range(SIZE)] for i in range(SIZE)]
    return board

# returns iterable of legal moves by given player in given gameState
def getLegalMoves(self, gameState, turnNum):

    moves = []
    for i in range(SIZE):
        for j in range(SIZE):
            move = (i, j)

            if getSquare(gameState, move) == 0:
                moves.append(move)

    return moves

# marks off square (i, j) with number given by turnNum
def applyMove(self, gameState, turnNum, move):

    setSquare(gameState, move, turnNum)

# checks if current player has any possible 3 in a row
def checkWin(self, gameState):

    winning_sets = []

    # adding rows
    for i in range(SIZE):
        currSet = []

        for j in range(SIZE):
            currSet.append((i, j))

        winning_sets.append(currSet)

    # adding columns
    for j in range(SIZE):
        currSet = []

        for i in range(SIZE):
            currSet.append((i, j))

        winning_sets.append(currSet)

    # adding both diagonals
    d1_set = []
    d2_set = []
    for i in range(SIZE):
        d1_set.append((i, i))
        d2_set.append((i, (SIZE - 1) - i))

    winning_sets.append(d1_set)
    winning_sets.append(d2_set)

    # print(winning_sets)

    # checks if turnNum player has any winning sets
    for ws in winning_sets:
        hasAll = [True for i in range(self.nPlayers)]

        for square in ws:
            sqVal = getSquare(gameState, square)

            for player_index in range(self.nPlayers):
                if not(player_index + 1 == sqVal):
                    hasAll[player_index] = False

        # check if any player has all of the given set
        for player_index in range(self.nPlayers):
            if hasAll[player_index]:
                return player_index + 1

    return False

# determines winner in case of no legal moves
def winsStalemate(self, gameState, turnNum):
    # player that goes second wins ties
    # makes the game "more interesting" (closer to balanced)
    return 2

# renders the game board
def render_gameState(self, gameState):

    # first renders in terms of a 2d array
    SQUARE_SIZE = 3
    square_center = (SQUARE_SIZE - 1) / 2

    arr_size = SIZE*(SQUARE_SIZE + 1) - 1
    render_arr = [[' ' for j in range(arr_size)] for i in range(arr_size)]

    square_chars = {
        0: ' ',
        1: 'X',
        2: 'O'
    }
    rowcol_chars = {
        (False, False): None,
        (True, False): '-',
        (False, True): '|',
        (True, True): '+',
    }

    # fills in render_arr
    for i in range(arr_size):
        for j in range(arr_size):
            # character to be added to render_arr
            currChar = ' '

            # location mod the relevant square
            row_index = i % (SQUARE_SIZE + 1)
            column_index = j % (SQUARE_SIZE + 1)

            # fills in center of squares
            if (row_index == square_center and column_index == square_center):
                square_i = (i - row_index) // (SQUARE_SIZE + 1)
                square_j = (j - column_index) // (SQUARE_SIZE + 1)
                square_coords = (square_i, square_j)

                currChar = square_chars[getSquare(gameState, square_coords)]

            # fills in rows/columns

            # indicator variables for rows/columns
            row_ind = (row_index == SQUARE_SIZE)
            col_ind = (column_index == SQUARE_SIZE)
            rowcol_ind = (row_ind, col_ind)

            rowcol_char = rowcol_chars[rowcol_ind]
            if (rowcol_char):
                currChar = rowcol_char

            # add currChar to array
            render_arr[i][j] += currChar

    # converts render_arr to string
    render_str = ""
    for i in range(arr_size):
        for j in range(arr_size):
            currChar = render_arr[i][j]
            render_str += currChar

        # end of line j
        render_str += "\n"

    return render_str

# assigning methods to Game obj
me.startState = startState
me.getLegalMoves = getLegalMoves
me.applyMove = applyMove
me.checkWin = checkWin
me.winsStalemate = winsStalemate
me.render_gameState = render_gameState
