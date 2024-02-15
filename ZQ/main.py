from board import Board
from notation import interpret_notation
from moves import (
    RookMovement,
    BishopMovement,
    UniversalMovementValidation,
    QueenMovement,
)
from copy import deepcopy
from utility import BoardUtils


# clean up imports in the final stage
# board = Board()
# starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# board.process_fen(starting_fen)
# notation = "nb1c3"

# board.move_piece(notation)
# print(board)

fen = "4r3/8/1q5b/8/3QQQ2/4K3/4Q3/4n3"
board = Board()
board.process_fen(fen)
print(board)
origin_pos, final_pos_piece = interpret_notation("Qe2e1")

bishop = board.board[origin_pos]
bishop_movement = QueenMovement(bishop)
valid_moves = bishop_movement.get_valid_moves(board.board)
print(valid_moves)
