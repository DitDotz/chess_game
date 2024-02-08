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
print(board)

notation = "nb8c6"

board.move_piece(notation)

print(board)

"""
Piece capturing is not properly
Iterate Through the Board: Traverse through the board to find pieces that match the piece type and color specified in the notation.

Check Valid Moves: Verify if the identified pieces can legally move to the destination square specified in the notation.

Disambiguate if Necessary: If there are multiple pieces of the same type that can move to the destination square, disambiguate by considering additional information such as the file or rank of the piece.
Implementing this logic requires more complex parsing and understanding of the chess board state. You would need to integrate algorithms to identify pieces, validate moves, and handle disambiguation.

"""
