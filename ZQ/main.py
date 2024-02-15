from board import Board
from notation import interpret_notation
from moves import RookMovement

# clean up imports in the final stage
# board = Board()
# starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# board.process_fen(starting_fen)
# # notation = input("please input a notation")  # be1g5
# notation = "nb1c3"

# board.move_piece(notation)
# print(board)


fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
board = Board()
board.process_fen("4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3")
print(board)
origin_pos, final_pos_piece = interpret_notation("Re2e1")
rook = board.board[origin_pos]
rook_movement = RookMovement(rook)
valid_moves = rook_movement.get_valid_moves(
    board.board, final_pos_piece.x, final_pos_piece.y
)
print(valid_moves)
# Re4e5
# But the move works in test_moves
# simulated board is not updating the rook movement
# piece_at_position should be a rook
