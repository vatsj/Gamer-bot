from .TwoPGame import TwoPGame

# to encode gameState as tuple
from .helpers import tuplify

# Game object representing the game tic-tac-toe
T3 = TwoPGame()


# template definitions for Game object
me = T3

# board size
SIZE = 3

EMPTY_SQUARE = 0

# helper functions

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

    board = [[EMPTY_SQUARE for j in range(SIZE)] for i in range(SIZE)]
    return board

# returns iterable of legal moves by given player in given gameState
def getLegalMoves(self, gameState, turnNum):

    moves = []
    for i in range(SIZE):
        for j in range(SIZE):
            move = (i, j)

            if getSquare(gameState, move) == EMPTY_SQUARE:
                moves.append(move)

    return moves

# returns length of allMoves list
def nMoves(self, allMoves):

    return len(allMoves)

# marks off square (i, j) with number given by turnNum
def applyMove(self, gameState, turnNum, move):

    setSquare(gameState, move, turnNum)

# overwrites square (i, j) with EMPTY_SQUARE
def undoMove(self, gameState, turnNum, move):

    # check for correct move
    if (getSquare(gameState, move) != turnNum):
        raise Exception("Incorrect args to T3 - undoMove!!!")

    setSquare(gameState, move, EMPTY_SQUARE)

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

# constants for rendering gameState
SQUARE_SIZE = 3
SQUARE_CHARS = {
    EMPTY_SQUARE: ' ',
    1: 'x',
    2: 'o'
}
ROWCOL_CHARS = {
    (False, False): None,
    (True, False): '-',
    (False, True): '|',
    (True, True): '+',
}

# renders the game board
def render_gameState(self, gameState):

    # first renders in terms of a 2d array
    square_center = (SQUARE_SIZE - 1) / 2

    arr_size = SIZE*(SQUARE_SIZE + 1) - 1
    render_arr = [[' ' for j in range(arr_size)] for i in range(arr_size)]

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

                currChar = SQUARE_CHARS[getSquare(gameState, square_coords)]

            # fills in rows/columns

            # indicator variables for rows/columns
            row_ind = (row_index == SQUARE_SIZE)
            col_ind = (column_index == SQUARE_SIZE)
            rowcol_ind = (row_ind, col_ind)

            rowcol_char = ROWCOL_CHARS[rowcol_ind]
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

# renders the game board filled with arbitrary info
# only handles info = [single-char array]
def render_gameInfo(self, gameState, info):

    # first renders in terms of a 2d array
    square_center = (SQUARE_SIZE - 1) / 2

    arr_size = SIZE*(SQUARE_SIZE + 1) - 1
    render_arr = [[' ' for j in range(arr_size)] for i in range(arr_size)]

    # keeps track of current elt of info
    info_index = 0

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

                currVal = getSquare(gameState, square_coords)
                if currVal != EMPTY_SQUARE:
                    currChar = SQUARE_CHARS[currVal]
                else:
                    currChar = str(info[info_index])
                    info_index += 1

            # fills in rows/columns

            # indicator variables for rows/columns
            row_ind = (row_index == SQUARE_SIZE)
            col_ind = (column_index == SQUARE_SIZE)
            rowcol_ind = (row_ind, col_ind)

            rowcol_char = ROWCOL_CHARS[rowcol_ind]
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

# encodes (boardState, turnNum)
def encode_posn(self, gameState, turnNum):

    encoded_gameState = tuplify(gameState)
    posn = (encoded_gameState, turnNum)

    # print(posn)
    return posn

# math helper fns for symmetry group
# G = D4 (dihedral group of a square/4-gon)
def fncomp(fn_list):

    # defining the composition of functions
    def comp(x):
        y_curr = x

        for fn_curr in fn_list[ : :-1]:
            y_curr = fn_curr(y_curr)

        return y_curr

    return comp

# converts between function and "tracker" forms
def fn2tracker(fn):
    # evaluates the fn to track square mapping
    tracker_board = [[(i, j) for j in range(SIZE)] for i in range(SIZE)]
    y_tracker_board = fn(tracker_board)

    return y_tracker_board

def tracker2fn(y_tracker):

    # hardcodes the fn as a consequence of the conversion
    def fn(gameBoard):

        y_gameBoard = startState(None)

        # fills in y_gameBoard with gameBoard elts,
        # indexed by y_tracker_board
        for i in range(SIZE):
            for j in range(SIZE):
                currSquare = (i, j)
                y_currSquare = getSquare(y_tracker, currSquare)

                currVal = getSquare(gameBoard, currSquare)
                setSquare(y_gameBoard, y_currSquare, currVal)

        return y_gameBoard

    return fn

# hardcodes a fn behavior to simplify computation
def hardcode_fn(fn):

    # hardcodes by converting between fn tracker form
    hardcoded_fn = tracker2fn(fn2tracker(fn))
    # print(hardcoded_fn)
    return hardcoded_fn

# defining rotate_CCW fn
y_tracker_rCCW = [[((SIZE - 1) - j, i) for j in range(SIZE)] for i in range(SIZE)]
rotate_CCW = tracker2fn(y_tracker_rCCW)

# defining flip_Xaxis fn
y_tracker_fXa = [[((SIZE - 1) - i, j) for j in range(SIZE)] for i in range(SIZE)]
flip_Xaxis = tracker2fn(y_tracker_fXa)

# identity fn on gameBoards
# returns identity tracker board, converted to fn

# defining ID fn
tracker = [[(i, j) for j in range(SIZE)] for i in range(SIZE)]
y_tracker_ID = tracker
ID = tracker2fn(y_tracker_ID)

# TESTING
# # defining testBoard
# testBoard = startState(None)
# squares_ind = [(0, 0), (0, 1)]
# char_ind = "+"
#
# for square in squares_ind:
#     setSquare(testBoard, square, char_ind)
# END TESTING

# encodes symmetry group of gameBoards
GROUP_STRUCTURE = (
    (rotate_CCW, 4),
    (flip_Xaxis, 2)
)

# helper function for constructing symmetry group
def construct_sym_group(G_S):

    # base case: if no generators, return ID fn
    if len(G_S) == 0:
        return [ID]

    curr_genmult = G_S[0]
    curr_generator, curr_mult = curr_genmult
    recursive_sym_group = construct_sym_group(G_S[1:])

    sym_group = []
    for mult in range(curr_mult):
        for rec_fn in recursive_sym_group:

            fn_list = mult * [curr_generator] + [rec_fn]
            curr_fn = fncomp(fn_list)
            sym_group.append(curr_fn)

    return sym_group

# constructs and hardcodes symmetry group
sym_group = construct_sym_group(GROUP_STRUCTURE)
hardcoded_sym_group = [hardcode_fn(fn) for fn in sym_group]

# testing

# test_fn = rotate_CCW
# print("rotate CCW: \n", test_fn(testBoard))
#
# for fn in hardcoded_sym_group:
#     currBoard = fn(testBoard)
#     print(currBoard)
#
# raise Exception("donezo")

# encodes equivalence class of posns under euclidean transformations
# compresses MC_dict size
def encode_posn_symmetric(self, gameState, turnNum):

    # computes equivalence class of gameState
    gS_equivClass = []
    for fn in sym_group:
        # print(fn, gameState)
        currBoard = fn(gameState)
        gS_equivClass.append(tuplify(currBoard))

    # encodes min of equivalence class
    equiv_rep = min(gS_equivClass)
    # print(equiv_rep)
    posn = (equiv_rep, turnNum)

    # print(posn)
    return posn

# assigning methods to Game obj
me.startState = startState
me.getLegalMoves = getLegalMoves
me.nMoves = nMoves
me.applyMove = applyMove
me.undoMove = undoMove
me.checkWin = checkWin
me.render_gameState = render_gameState
me.render_gameInfo = render_gameInfo
# me.encode_posn = encode_posn
me.encode_posn = encode_posn_symmetric
