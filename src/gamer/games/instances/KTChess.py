from .Game import Game

# imports chess library
import chess

"""
Represents game of "king-take chess"
same as normal chess, but win cond is taking the king as a piece
hopefully more direct to encode/learn than normal chess
NOTE: renders stalemate impossible during the game

docs for chess module found below:
https://github.com/niklasf/python-chess
"""

# game object
chess_game = Game()
# print(T3)
chess_game.nPlayers = 2

# dict: turnNum --> chess.Color
COLORS = {
    1: chess.WHITE,
    2: chess.BLACK,
}

# template definitions for Game object
me = chess_game

# returns the initial game state (upon starting a new game)
def startState(self):

    board = chess.Board()
    return board

# returns iterable of legal moves by given player in given board
def getLegalMoves(self, board, turnNum):

    # "pseudo-legal moves"
    # produces moves legal in king-take chess
    # possibly leaves king in check
    PL_moves = board.pseudo_legal_moves
    return list(PL_moves)

# size() fn is specific to python-chess interface
def nMoves(self, allMoves):
    return len(allMoves)

# applies move on turn turnNum to board
def applyMove(self, board, turnNum, move):

    # pushes current move to board
    board.push(move)

# overwrites square (i, j) with EMPTY_SQUARE
def undoMove(self, board, turnNum, move):

    # pops most recent move; takes in no arguments
    board.pop()

# checks if current player has any possible 3 in a row
def checkWin(self, board):

    # checks if king is taken
    for tN in COLORS.keys():

        # if either side missing a king, the other side wins
        if not(board.king(COLORS[tN])):
            winner = 3 - tN
            return winner

    # indicator for any type of "tied game"
    tie_ind = board.is_game_over() and not(board.is_checkmate())

    if tie_ind:
        # treat position as a stalemate, determine winner as stalemate winner
        # dummy value for turnNum
        return winsStalemate(self, board, None)

    # if no win detected, return False
    return False

# determines winner in case of no legal moves
def winsStalemate(self, board, turnNum):
    # player that goes second wins ties
    # makes the game "more interesting" (closer to balanced)
    return 2

# renders the game board
def render_board(self, board):
    return str(board)

# renders the game board filled with arbitrary info
# only handles info = [single-char array]
def render_gameBoard(self, board, info):

    # no good way to fill chess board with info
    # in particular, squares would need >1 entry
    pass

# encodes (boardState, turnNum)
def encode_posn(self, board, turnNum):

    encoded_board = board.fen()
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
me.winsStalemate = winsStalemate
me.render_board = render_board
me.render_gameBoard = render_gameBoard
me.encode_posn = encode_posn
