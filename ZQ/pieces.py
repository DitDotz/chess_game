from enum import Enum
from dataclasses import dataclass
from typing import Dict, Tuple, List


class Color(Enum):
    WHITE = 0
    BLACK = 1
    NONE = -1


class PieceType(Enum):
    EMPTY = "empty"
    PAWN = "pawn"
    ROOK = "rook"
    BISHOP = "bishop"
    QUEEN = "queen"
    KNIGHT = "knight"
    KING = "king"


# dictionary of fen as keys and PieceType as values
FEN_MAP: Dict[str, PieceType] = {
    "p": PieceType.PAWN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "q": PieceType.QUEEN,
    "k": PieceType.KING,
    "n": PieceType.KNIGHT,
}


PIECE_STR: Dict[PieceType, Tuple[str, str]] = {
    PieceType.EMPTY: (" ", " "),
    PieceType.PAWN: ("♙", "♟"),
    PieceType.ROOK: ("♖", "♜"),
    PieceType.BISHOP: ("♗", "♝"),
    PieceType.QUEEN: ("♕", "♛"),
    PieceType.KING: ("♔", "♚"),
    PieceType.KNIGHT: ("♘", "♞"),
}


Position = Tuple[int, int]


@dataclass
class Piece:
    x: int
    y: int
    color: Color = Color.NONE
    type: PieceType = PieceType.EMPTY

    @property
    def repr(self) -> str:
        if self.color == Color.WHITE:
            return PIECE_STR[self.type][1]

        elif self.color == Color.BLACK:
            return PIECE_STR[self.type][0]
        else:
            return PIECE_STR[self.type][0]

    @staticmethod
    def initialize_from_fen_char(x: int, y: int, fen: str) -> "Piece":
        color = Color.WHITE if fen.isupper() else Color.BLACK
        type = FEN_MAP[fen.lower()]
        return Piece(x, y, color, type)
