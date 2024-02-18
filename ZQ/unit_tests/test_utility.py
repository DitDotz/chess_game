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
from pieces import Piece, PieceType, Color, FEN_MAP
from board import Board
from notation import Notation
from utility import BoardUtils


def test_pawn_can_be_promoted_black_queen():
    fen = "4k3/P7/8/8/8/8/1p6/4K3"
    board = Board()
    board.process_fen(fen)

    notation = "pb2b1"
    board.move_piece(notation)
    expected_piece = Piece(x=7, y=1, color=Color.BLACK, type=PieceType.QUEEN)
    assert board.board[(7, 1)] == expected_piece


def test_pawn_can_be_promoted_white_queen():

    fen = "4k3/P7/8/8/8/8/1p6/4K3"
    board = Board()
    board.process_fen(fen)
    notation = "Pa7a8"
    board.move_piece(notation)
    expected_piece = Piece(x=0, y=0, color=Color.WHITE, type=PieceType.QUEEN)
    assert board.board[(0, 0)] == expected_piece
