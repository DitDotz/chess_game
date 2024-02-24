import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pieces import Piece, PieceType, Color, FEN_MAP
from board import Board


from pieces import Piece, Color
from utility import BoardUtils


def test_get_direction_vector_from_king_left():
    piece = Piece(x=0, y=0, type=PieceType.ROOK, color=Color.WHITE)
    king_x, king_y = 0, 1
    dx, dy = BoardUtils.get_direction_vector_from_king(piece, king_x, king_y)
    assert dx == 0
    assert dy == -1


def test_get_direction_vector_from_king_right():
    piece = Piece(x=0, y=2, type=PieceType.ROOK, color=Color.WHITE)
    king_x, king_y = 0, 1
    dx, dy = BoardUtils.get_direction_vector_from_king(piece, king_x, king_y)
    assert dx == 0
    assert dy == 1


def test_get_direction_vector_from_king_up():
    piece = Piece(x=0, y=0, type=PieceType.ROOK, color=Color.WHITE)
    king_x, king_y = 1, 0
    dx, dy = BoardUtils.get_direction_vector_from_king(piece, king_x, king_y)
    assert dx == -1
    assert dy == 0


def test_get_direction_vector_from_king_down():
    piece = Piece(x=2, y=0, type=PieceType.ROOK, color=Color.WHITE)
    king_x, king_y = 1, 0
    dx, dy = BoardUtils.get_direction_vector_from_king(piece, king_x, king_y)
    assert dx == 1
    assert dy == 0


def test_get_direction_vector_from_king_king_itself():
    piece = Piece(x=3, y=3, type=PieceType.KING, color=Color.WHITE)
    king_x, king_y = 3, 3
    dx, dy = BoardUtils.get_direction_vector_from_king(piece, king_x, king_y)
    assert dx == 0
    assert dy == 0


# def test_pawn_can_be_promoted_black_queen():
# fen = "4k3/P7/8/8/8/8/1p6/4K3"
# board = Board()
# board.process_fen(fen)
# board.move_made = 1
# board.expected_player = Color.BLACK

# notation = "pb2b1"
# board.move_piece(notation)
# expected_piece = Piece(x=7, y=1, color=Color.BLACK, type=PieceType.QUEEN)
# assert board.board[(7, 1)] == expected_piece


def test_pawn_can_be_promoted_white_queen():

    fen = "4k3/P7/8/8/8/8/1p6/4K3"
    board = Board()
    board.process_fen(fen)
    notation = "Pa7a8"
    board.move_piece(notation)
    expected_piece = Piece(x=0, y=0, color=Color.WHITE, type=PieceType.QUEEN)
    assert board.board[(0, 0)] == expected_piece
