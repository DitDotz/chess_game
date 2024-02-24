from typing import Tuple, Dict

from pieces import Piece, Color, PieceType


class KingValidation:
    """
    Utility class for validating the position of kings on the chessboard.
    """

    @staticmethod
    def find_king_position(
        board: Dict[Tuple[int, int], Piece], color: Color
    ) -> Tuple[int, int]:
        """
        Find the position of the king of the specified color on the given board.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.
            color (Color): The color of the king to find.

        Returns:
            Tuple[int, int]: The coordinates (x, y) of the king on the board.

        Raises:
            KingNotFound: If the king of the specified color is not found on the board.
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


class KingNotFound(Exception):
    """
    Exception raised when the king of a specified color is not found on the board.
    """

    def __init__(self, color: Color):
        self.color = color
        super().__init__(f"{color} king not found")
