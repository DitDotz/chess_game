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
board.process_fen("4r3/4k4")
rook_piece = board.board[(0, 4)]
print(board)

rook_movement = RookMovement(rook_piece)
valid_moves = rook_movement.get_valid_moves(board)
