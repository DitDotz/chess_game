from typing import Dict, Tuple

from pieces import Piece, PieceType, Color


class BoardUtils:

    @staticmethod
    def get_direction_vector_from_king(
        piece: Piece, king_x: int, king_y: int
    ) -> Tuple[int, int]:
        dx = -1 if king_x > piece.x else (1 if king_x < piece.x else 0)
        dy = -1 if king_y > piece.y else (1 if king_y < piece.y else 0)
        return dx, dy

    # Need to refactor this so it returns something that is unit testable
    @staticmethod
    def simulate_piece_move(
        simulated_board: Dict[Tuple[int, int], Piece],
        piece: Piece,
        new_x: int,
        new_y: int,
    ):
        simulated_board[(piece.x, piece.y)] = Piece(
            x=piece.x, y=piece.y, type=PieceType.EMPTY
        )
        updated_piece = Piece(x=new_x, y=new_y, type=piece.type, color=piece.color)
        simulated_board[(new_x, new_y)] = updated_piece

    @staticmethod
    def is_in_direct_contact_with_opposing_piece(
        piece_at_position: Piece,
        dx: int,
        dy: int,
    ) -> bool:
        # If it is not empty, then it must be the opposing color
        # if diagonal direction, check for opposing queen and bishop
        if abs(dx) == abs(dy) and piece_at_position.type in [
            PieceType.BISHOP,
            PieceType.QUEEN,
        ]:
            return True
        # If horizontal or vertical direction, check for opposing queen and rook
        # Condition works because dx and dy cannot be both zero at the same time
        elif (dx == 0 or dy == 0) and piece_at_position.type in [
            PieceType.QUEEN,
            PieceType.ROOK,
        ]:
            return True

        else:
            return False

    @staticmethod
    def promote_pawn_if_available(
        piece_to_check: Piece, board: Dict[Tuple[int], Piece]
    ) -> Dict[Tuple[int], Piece]:

        if (
            piece_to_check.type == PieceType.PAWN
            and piece_to_check.color == Color.WHITE
            and piece_to_check.x == 0
        ):

            board[(piece_to_check.x, piece_to_check.y)] = Piece(
                x=piece_to_check.x,
                y=piece_to_check.y,
                type=PieceType.QUEEN,
                color=Color.WHITE,
            )

            # Check if a black pawn reached the 8th rank
        elif (
            piece_to_check.type == PieceType.PAWN
            and piece_to_check.color == Color.BLACK
            and piece_to_check.x == 7
        ):

            board[(piece_to_check.x, piece_to_check.y)] = Piece(
                x=piece_to_check.x,
                y=piece_to_check.y,
                type=PieceType.QUEEN,
                color=Color.BLACK,
            )

        return board
