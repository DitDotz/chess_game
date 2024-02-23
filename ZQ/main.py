from board import Board
from notation import Notation
from moves import (
    RookMovement,
    BishopMovement,
    UniversalMovementValidation,
    QueenMovement,
    KnightMovement,
    PawnMovement,
    KingMovement,
)
from copy import deepcopy
from utility import BoardUtils
from pieces import FEN_MAP, Color

# clean up imports in the final stage
# if __name__ == "__main__":
# Infinite loop
# board = Board()
# starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# board.process_fen(starting_fen)
# print(board)

# # Gameloop
# while not board.king_in_checkmate:
#     notation = Notation.get_valid_notation(board.board)
#     board.move_piece(notation)
#     print(board)

#     if board.king_in_checkmate == True:
#         break

board = Board()
fen = "4r3/8/8/8/q7/8/R2P4/3K4"
board.process_fen(fen)
# valid_moves = board.get_all_valid_moves(color=Color.WHITE, board=board.board)
valid_moves = RookMovement(piece=board.board[(6, 0)]).get_valid_moves(board=board.board)
print(board)
print(valid_moves)

# rook should block or capture the queen
# test capture pinning piece

# check for checkmate
# checkmate is check + no valid moves available
# current way of checking for check does not cover situation whereby 2 pieces give checks at once

# check if king is in check, available moves are to move it out of check
# move king itself or use other piece to block
# reverse translator from grid to notation, and if invalid move is played, show valid_moves_list

# KingMovement is not implemented

# check_move_is_valid and get_valid_moves should be refactored
