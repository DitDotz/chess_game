from typing import List, Tuple, Dict

from pieces import Piece, Color, PieceType
from board import Board


class KingValidation:
    @staticmethod
    def find_king_position(
        board: Dict[Tuple[int, int], Piece], color: Color
    ) -> Tuple[int, int]:
        """
        Find the position of the king of the specified color on the given board.
        """
        for piece in board.values():
            if piece.type == PieceType.KING and piece.color == color:
                return (piece.x, piece.y)

        raise KingNotFound(color)


class KingNotFound(Exception):
    """Exception raised when the king of a specified color is not found on the board."""

    def __init__(self, color: Color):
        self.color = color
        super().__init__(f"King of color {color} is not found on the board")
