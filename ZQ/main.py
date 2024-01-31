# clean up imports in the final stage
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Tuple

from pieces import *
from board import *

# Initialize a grid filled with pieces
# data structure is a dictionary of a tuple of integers as the key
# and a Piece Class as the value

board = Board()

starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

position_map = board.process_fen(starting_fen)

pieces = PieceFactory.create_pieces_from_position_map(position_map)

print(board.board)
