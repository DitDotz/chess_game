from typing import Dict, Tuple
from copy import deepcopy

# import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from moves import (
    UniversalMovementValidation,
    RookMovement,
    BishopMovement,
    QueenMovement,
    KnightMovement,
)
from pieces import Piece, PieceType, Color
from board import Board
from notation import Notation
from utility import BoardUtils


def test_pawn_can_be_promoted_black_queen():
    # fen = '8/P7/8/8/8/8/1p6/8 w - - 0 1'
    # board = Board()
    # board.process_fen(fen)
    # board.move_piece()

    pass


def test_pawn_can_be_promoted_white_queen():

    # fen = '8/P7/8/8/8/8/1p6/8 w - - 0 1'
    # board = Board()
    # board.process_fen(fen)
    # board.move_piece()
    pass
