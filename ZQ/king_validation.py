import traceback
from typing import List, Tuple, Dict

from pieces import Piece, Color, PieceType


class KingValidation:
    @staticmethod
    def find_king_position(
        board: Dict[Tuple[int, int], Piece], color: Color
    ) -> Tuple[int, int]:
        """
        Find the position of the king of the specified color on the given board.
        """
        king_position = (None, None)  # Initialize king position to None

        for piece in board.values():
            if piece.type == PieceType.KING and piece.color == color:
                king_position = (piece.x, piece.y)
                break  # Exit the loop once the king is found

        # Raise KingNotFound if king position is not found
        if king_position == (None, None):
            raise KingNotFound(color)

        return king_position

    @staticmethod
    def king_in_check() -> bool:
        pass

    @staticmethod
    def king_in_checkmate() -> bool:
        pass


class KingNotFound(Exception):
    """Exception raised when the king of a specified color is not found on the board."""

    def __init__(self, color: Color):
        self.color = color
        super().__init__(f"{color} king not found")
