# clean up imports in the final stage
from pieces import *
from board import *

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

origin_pos, final_pos_piece = interpret_notation("Rd4d1")
print(origin_pos, final_pos_piece)

"""
Check Valid Moves: Verify if the identified pieces can legally move to the destination square specified in the notation.
"""
