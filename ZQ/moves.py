from typing import List, Tuple, Dict
from copy import deepcopy
from abc import ABC, abstractmethod
from pieces import Piece, Color, PieceType
from king_validation import KingValidation


class PieceMovement(ABC):
    def __init__(self, piece: Piece):
        self.piece = piece

    @abstractmethod
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
        pass


class KingMovement(PieceMovement):
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
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
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color
        new_x, new_y = None, None  # to edit

        if UniversalMovementValidation.is_pinned_to_own_king(x, y):
            return valid_moves

        # Define directions for rook movement: up, down, left, right
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

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
                        break
                    new_x, new_y = new_x + dx, new_y + dy
                else:
                    break

        return valid_moves


class KnightMovement(PieceMovement):
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
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
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        if UniversalMovementValidation.is_pinned_to_own_king(x, y):
            return valid_moves

        # Define directions for bishop movement: diagonals
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

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
                        break
                    new_x, new_y = new_x + dx, new_y + dy
                else:
                    break

        return valid_moves


class QueenMovement(PieceMovement):
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
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
                        break
                    new_x, new_y = new_x + dx, new_y + dy
                else:
                    break

        return valid_moves


class PawnMovement(PieceMovement):
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
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


class UniversalMovementValidation:
    @staticmethod
    def is_within_board(new_x: int, new_y: int) -> bool:
        return 0 <= new_x < 8 and 0 <= new_y < 8

    @staticmethod
    def is_not_occupied_by_allies(
        board: Dict[Tuple[int, int], Piece], new_x: int, new_y: int, color: Color
    ):
        piece_at_position = board[(new_x, new_y)]
        print(piece_at_position.color)

        return (
            piece_at_position.color != color
            or piece_at_position.type == PieceType.EMPTY
        )

    @staticmethod
    def is_pinned_to_own_king(
        piece: Piece, board: Dict[Tuple[int, int], Piece], new_x: int, new_y: int
    ) -> bool:

        color = piece.color

        king_x, king_y = KingValidation.find_king_position(board, color)
        print(king_x, king_y)

        # Determine the direction vector from the piece to its own king
        dx = 1 if king_x > piece.x else (-1 if king_x < piece.x else 0)
        dy = 1 if king_y > piece.y else (-1 if king_y < piece.y else 0)

        # Make a copy of the original board to simulate the move
        simulated_board = deepcopy(board)

        # Simulate the move of the piece on the simulated board
        simulated_board[(piece.x, piece.y)] = Piece(
            x=piece.x, y=piece.y, type=PieceType.EMPTY
        )

        updated_piece = Piece(x=new_x, y=new_y, type=piece.type, color=color)

        simulated_board[(new_x, new_y)] = updated_piece

        # Iterate in the direction of the king on the simulated board to check for potential pins
        x, y = piece.x + dx, piece.y + dy
        while UniversalMovementValidation.is_within_board(x, y):
            piece_at_position = simulated_board.get((x, y))

            if not UniversalMovementValidation.is_not_occupied_by_allies(
                board, x, y, color
            ):
                piece_at_position = board.get((x, y))
                if piece_at_position:
                    # if diagonal direction, check for opposing queen and bishop
                    if abs(dx) == abs(dy) and piece_at_position.type in [
                        PieceType.BISHOP,
                        PieceType.QUEEN,
                    ]:
                        return True
                    # if horizontal or vertical direction, check for opposing queen and rook
                    elif (dx == 0 or dy == 0) and piece_at_position.type in [
                        PieceType.QUEEN,
                        PieceType.ROOK,
                    ]:
                        return True

                    else:
                        break
                else:
                    break

            x += dx
            y += dy

        return False

    @staticmethod
    def is_king_in_check_after_king_move():
        pass

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
