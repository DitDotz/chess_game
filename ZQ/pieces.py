from enum import Enum
from dataclasses import dataclass
from typing import Dict, Tuple, List


class Color(Enum):
    """
    Enumeration representing the colors of chess pieces.

    Attributes:
        WHITE (int): The value representing the white color.
        BLACK (int): The value representing the black color.
        NONE (int): The value representing no color (for empty squares).
    """

    WHITE = 0
    BLACK = 1
    NONE = -1


class PieceType(Enum):
    """
    Enumeration representing the types of chess pieces.

    Attributes:
        EMPTY (str): Represents an empty square on the chessboard.
        PAWN (str): Represents a pawn piece.
        ROOK (str): Represents a rook piece.
        BISHOP (str): Represents a bishop piece.
        QUEEN (str): Represents a queen piece.
        KNIGHT (str): Represents a knight piece.
        KING (str): Represents a king piece.
    """

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
    """
    Represents a chess piece.

    Attributes:
        x (int): The x-coordinate of the piece on the chessboard.
        y (int): The y-coordinate of the piece on the chessboard.
        color (Color): The color of the piece (defaults to Color.NONE).
        type (PieceType): The type of the piece (defaults to PieceType.EMPTY).
        has_moved (bool): Indicates whether the piece has moved (defaults to False).
        en_passantable (bool): Indicates whether the piece is en passantable (defaults to False).
    """

    x: int
    y: int
    color: Color = Color.NONE
    type: PieceType = PieceType.EMPTY
    has_moved = False
    en_passantable = False  # only True for pawn that moved 2 spaces, and returns to False after 1 turn by opposite color

    @property
    def repr(self) -> str:
        """
        Get the string representation of the piece.

        Returns:
            str: The string representation of the piece based on its color and type.
        """

        if self.color == Color.WHITE:
            return PIECE_STR[self.type][1]

        elif self.color == Color.BLACK:
            return PIECE_STR[self.type][0]
        else:
            return PIECE_STR[self.type][0]

    @staticmethod
    def initialize_from_fen_char(x: int, y: int, fen: str) -> "Piece":
        """
        Initialize a Piece object from a FEN character.

        Args:
            x (int): The x-coordinate of the piece.
            y (int): The y-coordinate of the piece.
            fen (str): The FEN character representing the piece.

        Returns:
            Piece: A Piece object initialized from the given FEN character.
        """

        color = Color.WHITE if fen.isupper() else Color.BLACK
        type = FEN_MAP[fen.lower()]
        return Piece(x, y, color, type)
