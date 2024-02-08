# clean up imports in the final stage
from pieces import *
from board import *
from notation import interpret_notation

# Initialize a grid filled with pieces
# data structure is a dictionary of a tuple of integers as the key
# and a Piece Class as the value
# Generate a text repr of the board


board = Board()
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
board.process_fen(starting_fen)
# notation = input("please input a notation")  # be1g5
notation = "nb1c3"

board.move_piece(notation)
print(board)

"""
Check Valid Moves: Verify if the identified pieces can legally move to the destination square specified in the notation.
"""
