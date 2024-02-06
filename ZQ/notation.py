from typing import Tuple, Dict
from pieces import *


def interpret_notation(notation: str) -> Tuple[PieceType, Color, int, int]:
    """
    Interpret chess algebraic notation and return the piece type, color, x, and y coordinates.
    """
    # Extract the piece type, color, and destination coordinates from the notation
    piece_type: PieceType = PieceType.EMPTY
    color: Color = Color.NONE
    x, y = None, None

    # Handle notation with length 3
    if len(notation) == 3:
        piece_type = (
            PieceType.PAWN
        )  # By default, if only coordinates are given, it's a pawn move

        if notation[0].lower() in FEN_MAP:
            piece_type = FEN_MAP[notation[0].lower()]
        x = ord(notation[1]) - ord("a")
        y = 8 - int(notation[2])

    # Handle notation with length 4 (captures or disambiguated moves)
    elif len(notation) == 4:
        piece_type = FEN_MAP[notation[0].lower()]
        x = ord(notation[2]) - ord("a")
        y = 8 - int(notation[3])

    print(piece_type)
    color = Color.WHITE if notation[0].isupper() else Color.BLACK
    piece = Piece(x=x, y=y, color=color, type=piece_type)

    return piece


# Test the function
notation = "Nh4"
piece = interpret_notation(notation)
print(f"Interpreted notation {piece})")
