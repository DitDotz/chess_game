from typing import List, Tuple, Dict, Type
from copy import deepcopy
from abc import ABC, abstractmethod
from pieces import Piece, Color, PieceType
from king_validation import KingValidation
from utility import BoardUtils


class PieceMovement(ABC):
    def __init__(self, piece: Piece):
        self.piece = piece

    @abstractmethod
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        pass


class KingMovement(PieceMovement):
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color
        new_x, new_y = None, None  # to edit

        # Relative directions the king can move
        directions = [
            (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)
        ]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (
                UniversalMovementValidation.is_within_board(new_x, new_y)
                and UniversalMovementValidation.is_not_occupied_by_allies(
                    board, new_x, new_y, color
                )
                and not UniversalMovementValidation.is_king_in_check_after_king_move()
            ):
                valid_moves.append((new_x, new_y))

        return valid_moves


class RookMovement(PieceMovement):
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:

        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        # Define directions for rook movement: up, down, left, right
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            dir_x, dir_y = x + dx, y + dy
            simulated_board = deepcopy(board)
            # Simulate the move of the piece on the simulated board in available direction
            BoardUtils.simulate_piece_move(
                simulated_board=simulated_board,
                piece=self.piece,
                new_x=dir_x,
                new_y=dir_y,
            )

            while UniversalMovementValidation.is_within_board(dir_x, dir_y):

                # check original board
                if UniversalMovementValidation.is_not_occupied_by_allies(
                    board, dir_x, dir_y, color
                ):
                    # check using simulated board
                    if UniversalMovementValidation.is_pinned_to_own_king(
                        originalPiece=self.piece, board=simulated_board
                    ):
                        break

                    valid_moves.append((dir_x, dir_y))

                    # Stop moving in this direction if occupied by opposing piece
                    if UniversalMovementValidation.is_occupied_by_opposing(
                        simulated_board, dir_x, dir_y, color
                    ):
                        break

                    dir_x, dir_y = dir_x + dx, dir_y + dy

                else:
                    break

        return valid_moves


class KnightMovement(PieceMovement):
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        if UniversalMovementValidation.is_pinned_to_own_king(x, y):
            return valid_moves

        directions = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if UniversalMovementValidation.is_within_board(
                new_x, new_y
            ) and UniversalMovementValidation.is_not_occupied_by_allies(
                board, new_x, new_y, color
            ):
                valid_moves.append((new_x, new_y))

        return valid_moves


class BishopMovement(PieceMovement):
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        # Define directions for rook movement: up, down, left, right
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

        for dx, dy in directions:
            dir_x, dir_y = x + dx, y + dy
            # Make a copy of the original board to simulate the move
            simulated_board = deepcopy(board)

            # Simulate the move of the piece on the simulated board in available direction
            BoardUtils.simulate_piece_move(
                simulated_board=simulated_board,
                piece=self.piece,
                new_x=dir_x,
                new_y=dir_y,
            )

            while UniversalMovementValidation.is_within_board(dir_x, dir_y):

                # checked using original board
                if UniversalMovementValidation.is_not_occupied_by_allies(
                    board, dir_x, dir_y, color
                ):
                    # checked using simulation board
                    # this must update when the direction updates
                    # rename this to self_king_in_check_after_self_turn
                    if UniversalMovementValidation.is_pinned_to_own_king(
                        piece=self.piece, board=simulated_board
                    ):
                        break

                    valid_moves.append((dir_x, dir_y))

                    # Stop moving in this direction if occupied by opposing piece
                    if UniversalMovementValidation.is_occupied_by_opposing(
                        board, dir_x, dir_y, color
                    ):
                        break

                    dir_x, dir_y = dir_x + dx, dir_y + dy

                else:
                    break

        return valid_moves


class QueenMovement(PieceMovement):
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color
        new_x, new_y = None, None  # to edit

        if UniversalMovementValidation.is_pinned_to_own_king(x, y):
            return valid_moves

        directions = [
            (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)
        ]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            while UniversalMovementValidation.is_within_board(new_x, new_y):
                if UniversalMovementValidation.is_not_occupied_by_allies(
                    board, new_x, new_y, color
                ):
                    valid_moves.append((new_x, new_y))
                    # Stop moving in this direction if occupied by opposing piece
                    if UniversalMovementValidation.is_occupied_by_opposing(
                        board, new_x, new_y, color
                    ):
                        valid_moves.append((new_x, new_y))
                        break
                    new_x, new_y = new_x + dx, new_y + dy
                else:
                    break

        return valid_moves


class PawnMovement(PieceMovement):
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        if UniversalMovementValidation.is_pinned_to_own_king(x, y):
            return valid_moves

        direction = -1 if color == Color.WHITE else 1

        # Single move forward
        new_x, new_y = x + direction, y
        if (
            UniversalMovementValidation.is_within_board(new_x, new_y)
            and not board[new_x][new_y]
        ):
            valid_moves.append((new_x, new_y))

            # Double move forward on first move
            if not self.piece.has_moved:
                new_x, new_y = x + 2 * direction, y
                if (
                    UniversalMovementValidation.is_within_board(new_x, new_y)
                    and not board[new_x][new_y]
                ):
                    valid_moves.append((new_x, new_y))

        # Capture diagonally not sure if implementation is correct
        for dx in [-1, 1]:
            new_x, new_y = x + direction, y + dx
            if UniversalMovementValidation.is_within_board(
                new_x, new_y
            ) and UniversalMovementValidation.is_occupied_by_opposing(
                board, new_x, new_y, color
            ):
                valid_moves.append((new_x, new_y))

        return valid_moves


# Unit test successful
class UniversalMovementValidation:
    @staticmethod
    def is_within_board(new_x: int, new_y: int) -> bool:
        return 0 <= new_x < 8 and 0 <= new_y < 8

    @staticmethod
    def is_not_occupied_by_allies(
        board: Dict[Tuple[int, int], Piece], new_x: int, new_y: int, color: Color
    ):
        """
        Returns true if its empty squares or opposing color piece
        Implementation is taking movement into consideration only
        """
        piece_at_position = board[(new_x, new_y)]

        return (
            piece_at_position.color != color
            or piece_at_position.type == PieceType.EMPTY
        )

    # board refers to simulated board across in this function below
    @staticmethod
    def is_pinned_to_own_king(
        originalPiece: Piece, board: Dict[Tuple[int, int], Piece]
    ) -> bool:

        # Find position of king in simulated position
        king_x, king_y = KingValidation.find_king_position(board, originalPiece.color)

        # Determine the direction vector from the king to the piece being moved in original position
        # if piece moved is the king itself, then check all directions
        dx, dy = BoardUtils.get_direction_vector_from_king(
            piece=originalPiece, king_x=king_x, king_y=king_y
        )

        if dx == 0 and dy == 0:
            print("checks for king itself not implemented yet")
            return True

        # Iterate from the direction of the king on the simulated board to check for potential pins
        x, y = king_x + dx, king_y + dy

        while UniversalMovementValidation.is_within_board(x, y):
            piece_at_position = board.get((x, y))

            if UniversalMovementValidation.is_not_occupied_by_allies(
                board, x, y, originalPiece.color
            ):

                piece_at_position = board.get((x, y))

                # If it returns true, it can either be the opposing color or empty.
                # So your check should be if it is not empty

                # if its the opposing color
                if piece_at_position.type != PieceType.EMPTY:

                    if BoardUtils.is_in_direct_contact_with_opposing_piece(
                        piece_at_position=piece_at_position, dx=dx, dy=dy
                    ):
                        return True

                    else:
                        break
                else:
                    x += dx
                    y += dy

            else:
                break

        # Implement for when king itself has moved

        return False

    @staticmethod
    def is_occupied_by_opposing(
        board: Dict[Tuple[int, int], Piece], new_x: int, new_y: int, color: Color
    ) -> bool:
        """
        Check if the square at the given coordinates is occupied by an opposing piece.
        """
        piece_at_position = board.get((new_x, new_y))

        # Check if the square is occupied by an opposing piece
        return (
            piece_at_position is not None
            and piece_at_position.color != color
            and piece_at_position.type != PieceType.EMPTY
        )


PIECE_MOVE_MAP: Dict[PieceType, Type[PieceMovement]] = {
    PieceType.PAWN: PawnMovement,
    PieceType.ROOK: RookMovement,
    PieceType.BISHOP: BishopMovement,
    PieceType.QUEEN: QueenMovement,
    PieceType.KING: KingMovement,
    PieceType.KNIGHT: KnightMovement,
}
