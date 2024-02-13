from board import Board

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
board.process_fen(fen)
print(board)
board.move_piece()
print(board)

# Re4e5
# But the move works in test_moves
# simulated board is not updating the rook movement
# piece_at_position should be a rook
