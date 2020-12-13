from .TwoPGame import TwoPGame

# imports CD_LinkedList Node type
from .helpers import CD_Node, PosVec
# to encode gameState as tuple
from .helpers import tuplify

import copy

"""
Represents game of "Go
Win cond: have more stones than your opponent once board fills up
simple heuristic: (your stones) - (opponent stones)

gameState = {
"board": [[CD_Node]],
"recorded_moves": [[PosVec, {dir: deleted?}]]
"nTiles": [color_nTiles]
}
"""

# game object
go_game = TwoPGame()

# n x n go board
SIZE = 9
PosVec.SIZE = SIZE

# value for an empty square
EMPTY_SQUARE = 0

# template definitions for Game object
me = go_game


DISP_VECS = {
    "north": PosVec(-1, 0),
    "east": PosVec(0, 1),
    "south": PosVec(1, 0),
    "west": PosVec(0, -1),
}

# returns the initial game state (upon starting a new game)
def startState(self):

    # initializes board with no linkings
    board = [[CD_Node(EMPTY_SQUARE) for j in range(SIZE)] for i in range(SIZE)]

    # linking up board
    for i in range(SIZE):
        for j in range(SIZE):

            # finds current square
            curr_posVec = PosVec(i, j)
            curr_node = curr_posVec.indexInto(board)

            # links up to adjacent squares
            for dir in CD_Node.ADJACENCY_DIRS:
                target_posVec = curr_posVec.add(DISP_VECS[dir])
                target_node = target_posVec.indexInto(board)

                # links curr_node to target_node
                curr_node.setAdjacent(dir, target_node)

    # initializing values for beginning of game
    recorded_moves = []
    nTiles = [0, 0]

    # constructs gameState from component properties
    gameState = {
        "board": board,
        "recorded_moves": recorded_moves,
        "nTiles": nTiles,
    }
    return gameState

# print(startState(None)["board"][0][0])

# returns iterable of legal moves by given player in given board
def getLegalMoves(self, gameState, turnNum):

    board = gameState["board"]

    # constructs list of PosVec-s of valid moves
    allMoves = []
    for i in range(SIZE):
        for j in range(SIZE):
            move = PosVec(i, j)

            if move.indexInto(board).value == EMPTY_SQUARE:
                allMoves.append(move)

    return allMoves

# size() fn is specific to python-chess interface
def nMoves(self, allMoves):
    return len(allMoves)

"""
helper methods for applying/undoing moves
determines contiguous blobs of go pieces for capturing
"""

# finds contiguous blob of squares sharing value w repSquare
# returns (blob, perimeter) tuple
def getBlobPerimeter(self, repSquare, blobValue):

    if not(blobValue):
        blobValue = repSquare.value
    pass

# checks if all squares in squareSet are same color
# short-circuit evaluates
def checkMonocolor(self, squareSet, color):

    for square in squareSet:
        # if not that color, return false immediately
        if square.value != color:
            return False

    # if all are that color, return true
    return True

# overwrites values from each square in squareSet iterable
# doesn't check for values in squareSet --> be careful of input blob!
def setBlob(self, squareSet, value):

    for square in squareSet:
        square.value = value

# removes values from each square in squareSet iterable
def captureBlob(self, squareSet):

    setBlob(self, squareSet, EMPTY_SQUARE)

# applies move on turn turnNum to board
def applyMove(self, gameState, turnNum, move):

    board = gameState["board"]
    recorded_moves = gameState["moves"]
    nTiles = gameState["nTiles"]

    # sets square to value turnNum
    square = move.indexInto(board)
    square.value = turnNum

    # records move and tile counts

    # key/value pairs inserted during capturing step
    deletion_dirs = {}
    recorded_move = [move, deletion_dirs]
    recorded_moves.append(recorded_move)

    nTiles[turnNum - 1] += 1

    # detects and records blob captures

    otherTurnNum = self.otherPlayer(turnNum)

    adjacent_blobs = {}
    # marks whether blob in given direction will be captured
    capture_markers = {}
    for dir in CD_Node.ADJACENCY_DIRS:
        adj_posVec = move.add(DISP_VECS[dir])
        adj_node = adj_posVec.indexInto(board)

        # checks if blob has already been explored
        alreadyExplored = False
        for prev_dir in adjacent_blobs.keys():
            prev_blob = adjacent_blobs[prev_dir]

            # if already explored, fill in the information
            if adj_node in prev_blob:
                alreadyExplored = True

                adjacent_blobs[dir] = prev_blob
                # don't add redundant capture markers
                capture_markers[dir] = False

        if not(alreadyExplored):

            # finds adjacent blob and perimeter
            currBlob, currPerimeter = getBlobPerimeter(self, adj_node, otherTurnNum)
            adjacent_blobs[dir] = currBlob

            # checks for capture by seeing if perimeter is monocolor
            curr_CM = checkMonocolor(self, currPerimeter, otherTurnNum)
            capture_markers[dir] = curr_CM

            # if not already explored and capturable, then apply and record capture
            if currCM:
                captureBlob(self, currBlob)
                nTiles[otherTurnNum] -= len(currBlob)

    # records captures in recorded_moves info
    deletion_dirs = capture_markers

# overwrites square (i, j) with EMPTY_SQUARE
# TODO: undo deletion steps? needs additional info to work
def undoMove(self, ganeState, turnNum, move):

    board = gameState["board"]
    recorded_moves = gameState["moves"]
    nTiles = gameState["nTiles"]

    # pops most recent move (efficient since lists work like LIFO queues)
    lastMove = board.pop()
    move, deletion_dirs = lastMove

    # undoes the move and resulting captures

    # moved square must have been empty before move
    move.indexInto(board).value = EMPTY_SQUARE
    nTiles[turnNum - 1] -= 1

    otherTurnNum = self.otherPlayer(turnNum)

    for dir in CD_Node.ADJACENCY_DIRS:
        curr_CM = capture_markers[dir]

        if curr_CM:
            adj_posVec = move.add(DISP_VECS[dir])
            adj_node = adj_posVec.indexInto(board)

            # captured blob should be empty anyways, specifying EMPTY_SQUARE is redundant
            captured_blob = getBlobPerimeter(self, adj_node, EMPTY_SQUARE)
            setBlob(self, captured_blob, otherTurnNum)
            nTiles[otherTurnNum - 1] += len(captured_blob)

total_nTiles = (SIZE + 1)**2

# checks if either player fills up more than half the board with tiles
def checkWin(self, gameState):

    nTiles = gameState["nTiles"]

    # checks if either player has more than half the board
    for turnNum in range(game.nPlayers):
        if nTiles[turnNum - 1] >= total_nTiles / 2:
            return turnNum

    # if not, returns false
    return False

# helper fn for rendering go board
def render_board(board):

    # to construct the game board around
    retstr = ""

    retstr += "~"*10 + "\n"
    for i in range(SIZE):
        for j in range(SIZE):
            # finds current square
            curr_posVec = PosVec(i, j)
            curr_node = curr_posVec.indexInto(board)

            retstr += str(curr_node)

        # after row of board, add new line
        retstr += "\n"
    retstr += "~"*10 + "\n"

    return retstr

# renders the game board
def render_gameState(self, gameState):

    board = gameState["board"]

    return render_board(board)

# renders the game board filled with arbitrary info
# only handles info = [single-char array]
def render_gameInfo(self, gameState, info):

    board = copy.deepcopy(gameState["board"])

    for i in range(SIZE):
        for j in range(SIZE):
            curr_posVec = curr_posVec.add(DISP_VECS[dir])
            curr_node = curr_posVec.indexInto(board)

            # if no piece on the square <--> legal move
            # then paste in value from info
            if curr_node.value == EMPTY_SQUARE:
                curr_node.value = curr_posvec.indexInto(info)

    # render board filled in with info
    return render_board(board)

# encodes (boardState, turnNum)
def encode_posn(self, gameState, turnNum):

    encoded_gameState = tuplify(gameState)
    posn = (encoded_board, turnNum)

    # print(board)
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
me.encode_posn = encode_posn
