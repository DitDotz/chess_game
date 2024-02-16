from board import Board
from notation import Notation
from moves import (
    RookMovement,
    BishopMovement,
    UniversalMovementValidation,
    QueenMovement,
    KnightMovement,
)
from copy import deepcopy
from utility import BoardUtils
from pieces import FEN_MAP

# clean up imports in the final stage

# Infinite loop
board = Board()
starting_fen = "8/P7/8/8/8/8/1p6/8"
board.process_fen(starting_fen)
print(board)

# Gameloop
while not board.king_in_checkmate:
    notation = Notation.get_valid_notation(board.board)
    board.move_piece(notation)
    print(board)

    if board.king_in_checkmate == True:
        break

# fen = "8/P7/8/8/8/8/1p6/8 w - - 0 1"
# board = Board()
# board.process_fen(fen)

# notation = "pb2b1"
# board.move_piece(notation)
# print(board)

# check for checkmate
# checkmate is check + no valid moves available
# current way of checking for check does not cover situation whereby 2 pieces give checks at once

# check if king is in check, available moves are to move it out of check
# move king itself or use other piece to block
# reverse translator from grid to notation, and if invalid move is played, show valid_moves_list

# KingMovement is not implemented

# check_move_is_valid and get_valid_moves should be refactored
