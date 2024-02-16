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


# clean up imports in the final stage
board = Board()
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
board.process_fen(starting_fen)
print(board)

# Gameloop
king_in_checkmate = False

while not king_in_checkmate:
    board.move_piece()
    print(board)

# notation = "nb1c3"
# board.move_piece(notation)
# print(board)

# fen = "4r3/8/1q5b/8/3NNN2/4K3/4N3/4n3"
# board = Board()
# board.process_fen(fen)
# print(board)
# origin_pos, final_pos_piece = interpret_notation("Ne2e1")

# knight = board.board[origin_pos]
# knight_movement = KnightMovement(knight)
# valid_moves = knight_movement.get_valid_moves(board.board)
# print(valid_moves)

# check for checkmate
# checkmate is check + no valid moves available
# current way of checking for check does not cover situation whereby 2 pieces give checks at once

# check if king is in check, available moves are to move it out of check
# move king itself or use other piece to block
# reverse translator from grid to notation, and if invalid move is played, show valid_moves_list

# KingMovement is not implemented
