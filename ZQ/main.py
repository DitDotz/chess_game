# clean up imports in the final stage
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Tuple

from pieces import *
from board import *

# Initialize a grid filled with pieces
# data structure is a dictionary of a tuple of integers as the key
# and a Piece Class as the value
# Generate a text repr of the board


board = Board()
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
board.process_fen(starting_fen)
piece_to_move = board.board[(0, 1)]
board.move_piece(piece_to_move, 2, 3)
print(board.board[(2, 3)])
