import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from typing import Dict, Tuple
from pieces import Piece, Color, PieceType
from king_validation import KingValidation, KingNotFound


def test_find_king_position():
    # Test finding the white king

    board = {
        (0, 0): Piece(0, 0, type=PieceType.KING, color=Color.WHITE),
        (7, 7): Piece(7, 7, type=PieceType.KING, color=Color.BLACK),
    }
    white_king_pos = KingValidation.find_king_position(board, Color.WHITE)
    assert white_king_pos == (0, 0)

    # Test finding the black king
    black_king_pos = KingValidation.find_king_position(board, Color.BLACK)
    assert black_king_pos == (7, 7)


def test_find_king_position_no_kings_found():

    board = {
        (0, 0): Piece(0, 0, PieceType.EMPTY, Color.NONE),
        (7, 7): Piece(7, 7, PieceType.EMPTY, Color.NONE),
    }
    # Test finding kings when none exist (expecting KingNotFound exception)
    with pytest.raises(KingNotFound):
        KingValidation.find_king_position(board, Color.WHITE)

    with pytest.raises(KingNotFound):
        KingValidation.find_king_position(board, Color.BLACK)
