from board import Board
from notation import interpret_notation
from moves import RookMovement, BishopMovement, UniversalMovementValidation
from copy import deepcopy
from utility import BoardUtils


# clean up imports in the final stage
# board = Board()
# starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# board.process_fen(starting_fen)
# notation = "nb1c3"

# board.move_piece(notation)
# print(board)

fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
board = Board()
board.process_fen("4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3")
origin_pos, final_pos_piece = interpret_notation("Re2a2")
piece_to_move = board.board[origin_pos]
simulated_board = deepcopy(board.board)
# Simulate the move of the piece on the simulated board in available direction
BoardUtils.simulate_piece_move(
    simulated_board=simulated_board,
    piece=piece_to_move,
    new_x=final_pos_piece.x,
    new_y=final_pos_piece.y,
)

print(
    UniversalMovementValidation.is_pinned_to_own_king(
        originalPiece=piece_to_move, board=simulated_board
    )
)
