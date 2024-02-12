# clean up imports in the final stage
from pieces import *
from board import *
from moves import *

# board = Board()
# starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# board.process_fen(starting_fen)
# # notation = input("please input a notation")  # be1g5
# notation = "nb1c3"

# board.move_piece(notation)
# print(board)


# fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"

board = Board()
board.process_fen("4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3")
print(board)


origin_pos, final_pos_piece = interpret_notation("Re4e6")
piece_to_move = board.board[origin_pos]


UniversalMovementValidation.is_pinned_to_own_king(
    piece=piece_to_move,
    board=board.board,
    new_x=final_pos_piece.x,
    new_y=final_pos_piece.y,
)


"""
Check Valid Moves: Verify if the identified pieces can legally move to the destination square specified in the notation.
"""
