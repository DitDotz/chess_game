from typing import List, Tuple, Dict, Type
from copy import deepcopy
from abc import ABC, abstractmethod
from pieces import Piece, Color, PieceType
from king_validation import KingValidation
from utility import BoardUtils


class PieceMovement(ABC):
    """
    Abstract class for defining movement rules of chess pieces.

    Attributes:
        piece (Piece): The piece for which movement rules are defined.
    """

    def __init__(self, piece: Piece):
        """Initialize the PieceMovement object."""
        self.piece = piece

    @abstractmethod
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        """
        Get the valid moves for the piece on the given board.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.

        Returns:
            List[Tuple[int, int]]: A list of valid moves for the piece.
        """
        pass


class KingMovement(PieceMovement):
    """
    Defines movement rules for the king piece.

    Inherits from PieceMovement.
    """

    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        """
        Get the valid moves for the king on the given board.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.

        Returns:
            List[Tuple[int, int]]: A list of valid moves for the king.
        """

        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        # Relative directions the king can move
        directions = [
            (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)
        ]

        for dx, dy in directions:
            dir_x, dir_y = x + dx, y + dy
            if UniversalMovementValidation.is_within_board(
                dir_x, dir_y
            ) and UniversalMovementValidation.is_not_occupied_by_allies(
                board, dir_x, dir_y, color
            ):
                simulated_board = deepcopy(board)
                # Simulate the move of the piece on the simulated board in available direction
                BoardUtils.simulate_piece_move(
                    simulated_board=simulated_board,
                    piece=self.piece,
                    new_x=dir_x,
                    new_y=dir_y,
                )
                if not UniversalMovementValidation.is_king_in_check(
                    color=color, board=simulated_board
                ):
                    valid_moves.append((dir_x, dir_y))

        return valid_moves


class RookMovement(PieceMovement):
    """
    Defines movement rules for the rook piece.

    Inherits from PieceMovement.
    """

    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        """
        Get the valid moves for the rook on the given board.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.

        Returns:
            List[Tuple[int, int]]: A list of valid moves for the rook.
        """

        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        # Define directions for rook movement: up, down, left, right
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:

            dir_x, dir_y = x + dx, y + dy

            while UniversalMovementValidation.is_within_board(dir_x, dir_y):

                # check original board
                if UniversalMovementValidation.is_not_occupied_by_allies(
                    board, dir_x, dir_y, color
                ):
                    valid_moves.append((dir_x, dir_y))

                    if UniversalMovementValidation.is_occupied_by_opposing(
                        board, dir_x, dir_y, color
                    ):
                        break

                    dir_x, dir_y = dir_x + dx, dir_y + dy

                else:
                    break

        validated_moves = []
        for move in valid_moves:
            simulated_board = deepcopy(board)
            # Simulate the move of the piece on the simulated board in available direction
            BoardUtils.simulate_piece_move(
                simulated_board=simulated_board,
                piece=self.piece,
                new_x=move[0],
                new_y=move[1],
            )

            # check using simulated board
            if not UniversalMovementValidation.is_king_in_check(
                color=color, board=simulated_board
            ):
                validated_moves.append(move)

        return validated_moves


class KnightMovement(PieceMovement):
    """
    Defines movement rules for the knight piece.

    Inherits from PieceMovement.
    """

    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        """
        Get the valid moves for the knight on the given board.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.

        Returns:
            List[Tuple[int, int]]: A list of valid moves for the knight.
        """

        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

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
                    if UniversalMovementValidation.is_king_in_check(
                        color=color, board=simulated_board
                    ):
                        break

                    valid_moves.append((dir_x, dir_y))

                break

        return valid_moves


class BishopMovement(PieceMovement):
    """
    Defines movement rules for the bishop piece.

    Inherits from PieceMovement.
    """

    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        """
        Get the valid moves for the bishop on the given board.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.

        Returns:
            List[Tuple[int, int]]: A list of valid moves for the bishop.
        """

        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        # Define directions for rook movement: up, down, left, right
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

        for dx, dy in directions:

            dir_x, dir_y = x + dx, y + dy

            while UniversalMovementValidation.is_within_board(dir_x, dir_y):

                # check original board
                if UniversalMovementValidation.is_not_occupied_by_allies(
                    board, dir_x, dir_y, color
                ):
                    valid_moves.append((dir_x, dir_y))

                    if UniversalMovementValidation.is_occupied_by_opposing(
                        board, dir_x, dir_y, color
                    ):
                        break

                    dir_x, dir_y = dir_x + dx, dir_y + dy

                else:
                    break

        validated_moves = []
        for move in valid_moves:
            simulated_board = deepcopy(board)
            # Simulate the move of the piece on the simulated board in available direction
            BoardUtils.simulate_piece_move(
                simulated_board=simulated_board,
                piece=self.piece,
                new_x=move[0],
                new_y=move[1],
            )

            # check using simulated board
            if not UniversalMovementValidation.is_king_in_check(
                color=color, board=simulated_board
            ):
                validated_moves.append(move)

        return validated_moves


class QueenMovement(PieceMovement):
    """
    Defines movement rules for the queen piece.

    Inherits from PieceMovement.
    """

    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        """
        Get the valid moves for the queen on the given board.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.

        Returns:
            List[Tuple[int, int]]: A list of valid moves for the queen.
        """

        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        # Define directions for rook movement: up, down, left, right
        directions = [
            (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)
        ]
        for dx, dy in directions:

            dir_x, dir_y = x + dx, y + dy

            while UniversalMovementValidation.is_within_board(dir_x, dir_y):

                # check original board
                if UniversalMovementValidation.is_not_occupied_by_allies(
                    board, dir_x, dir_y, color
                ):
                    valid_moves.append((dir_x, dir_y))

                    if UniversalMovementValidation.is_occupied_by_opposing(
                        board, dir_x, dir_y, color
                    ):
                        break

                    dir_x, dir_y = dir_x + dx, dir_y + dy

                else:
                    break

        validated_moves = []
        for move in valid_moves:
            simulated_board = deepcopy(board)
            # Simulate the move of the piece on the simulated board in available direction
            BoardUtils.simulate_piece_move(
                simulated_board=simulated_board,
                piece=self.piece,
                new_x=move[0],
                new_y=move[1],
            )

            # check using simulated board
            if not UniversalMovementValidation.is_king_in_check(
                color=color, board=simulated_board
            ):
                validated_moves.append(move)

        return validated_moves


class PawnMovement(PieceMovement):
    """
    Defines movement rules for the pawn piece.

    Inherits from PieceMovement.
    """

    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
        """
        Get the valid moves for the pawn on the given board.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.

        Returns:
            List[Tuple[int, int]]: A list of valid moves for the queen.
        """

        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        if (self.piece.color == Color.WHITE and self.piece.x != 6) or (
            self.piece.color == Color.BLACK and self.piece.x != 1
        ):
            self.piece.has_moved = True

        # assumes white is at the bottom of the board
        direction = -1 if color == Color.WHITE else 1

        # Conditions for single move forward
        new_x, new_y = x + direction, y
        if (
            UniversalMovementValidation.is_within_board(new_x, new_y)
            and board[new_x, new_y].type == PieceType.EMPTY
        ):
            # Simulate the move on a temporary board
            simulated_board = deepcopy(board)
            simulated_board[new_x, new_y] = self.piece
            simulated_board[x, y] = Piece(
                x, y, PieceType.EMPTY
            )  # Update original position

            # Check for pinning to own king
            if not UniversalMovementValidation.is_king_in_check(
                self.piece.color, simulated_board
            ):
                valid_moves.append((new_x, new_y))

                # Double move forward on first move and if there are empty squares in both squares
                if not self.piece.has_moved:
                    new_x, new_y = x + 2 * direction, y

                    if (
                        UniversalMovementValidation.is_within_board(new_x, new_y)
                        and board[new_x, new_y].type == PieceType.EMPTY
                        and board[new_x - direction, new_y].type == PieceType.EMPTY
                    ):
                        # Simulate the move
                        simulated_board[new_x, new_y] = self.piece
                        simulated_board[x, y] = Piece(
                            x, y, PieceType.EMPTY
                        )  # Update original position

                        # Check for pinning to own king
                        if not UniversalMovementValidation.is_king_in_check(
                            self.piece.color, simulated_board
                        ):
                            valid_moves.append((new_x, new_y))

        # Conditions for diagonal capture
        for dy in [-1, 1]:
            new_x, new_y = x + direction, y + dy
            if UniversalMovementValidation.is_within_board(
                new_x, new_y
            ) and UniversalMovementValidation.is_occupied_by_opposing(
                board, new_x, new_y, color
            ):
                # Simulate the move
                simulated_board = deepcopy(board)
                simulated_board[new_x, new_y] = self.piece
                simulated_board[x, y] = Piece(
                    x, y, PieceType.EMPTY
                )  # Update original position

                # Check for pinning to own king
                if not UniversalMovementValidation.is_king_in_check(
                    self.piece.color, simulated_board
                ):
                    valid_moves.append((new_x, new_y))

        # Conditions for en-passant
        dy = [1, -1]
        if self.piece.color == Color.WHITE and self.piece.x == 3:
            for y in dy:
                if (
                    (
                        board[self.piece.x, self.piece.y + y].type == PieceType.PAWN
                        or board[self.piece.x, self.piece.y - y].type == PieceType.PAWN
                    )
                    and board[self.piece.x, self.piece.y + y].color == Color.BLACK
                    and board[self.piece.x, self.piece.y + y].en_passantable
                ):
                    new_x, new_y = self.piece.x + direction, self.piece.y + y
                    # Simulate the move
                    simulated_board = deepcopy(board)
                    simulated_board[new_x, new_y] = self.piece
                    simulated_board[x, y] = Piece(
                        x, y, PieceType.EMPTY
                    )  # Update original position

                    # Check for pinning to own king
                    if not UniversalMovementValidation.is_king_in_check(
                        self.piece.color, simulated_board
                    ):

                        valid_moves.append((new_x, new_y))

        elif self.piece.color == Color.BLACK and self.piece.x == 4:
            for y in dy:
                if (
                    (
                        board[self.piece.x, self.piece.y + y].type == PieceType.PAWN
                        or board[self.piece.x, self.piece.y - y].type == PieceType.PAWN
                    )
                    and board[self.piece.x, self.piece.y + y].color == Color.WHITE
                    and board[self.piece.x, self.piece.y + y].en_passantable
                ):
                    new_x, new_y = self.piece.x + direction, self.piece.y + y
                    # Simulate the move
                    simulated_board = deepcopy(board)
                    simulated_board[new_x, new_y] = self.piece
                    simulated_board[x, y] = Piece(
                        x, y, PieceType.EMPTY
                    )  # Update original position

                    # Check for pinning to own king
                    if not UniversalMovementValidation.is_king_in_check(
                        self.piece.color, simulated_board
                    ):

                        valid_moves.append((new_x, new_y))

        return valid_moves


class UniversalMovementValidation:
    """
    Utility class for validating movement rules universally applicable to chess pieces.
    """

    @staticmethod
    def is_within_board(new_x: int, new_y: int) -> bool:
        """
        Check if the given coordinates are within the boundaries of the chessboard.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        Returns:
            bool: True if the coordinates are within the board, False otherwise.
        """
        return 0 <= new_x < 8 and 0 <= new_y < 8

    # Used on original board
    @staticmethod
    def is_not_occupied_by_allies(
        board: Dict[Tuple[int, int], Piece], new_x: int, new_y: int, color: Color
    ):
        """
        Check if the target position is not occupied by a piece of the same color.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.
            x (int): The x-coordinate of the target position.
            y (int): The y-coordinate of the target position.
            color (Color): The color of the piece attempting to move.

        Returns:
            bool: True if the target position is not occupied by allies, False otherwise.
        """

        piece_at_position = board[(new_x, new_y)]

        return (
            piece_at_position.color != color
            or piece_at_position.type == PieceType.EMPTY
        )

    # operated on simulated board (not sure if there is any difference)
    @staticmethod
    def is_occupied_by_opposing(
        board: Dict[Tuple[int, int], Piece], new_x: int, new_y: int, color: Color
    ) -> bool:
        """
        Check if the target position is occupied by a piece of the opposing color.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.
            x (int): The x-coordinate of the target position.
            y (int): The y-coordinate of the target position.
            color (Color): The color of the piece attempting to move.

        Returns:
            bool: True if the target position is occupied by an opposing piece, False otherwise.
        """
        piece_at_position = board.get((new_x, new_y))

        # Check if the square is occupied by an opposing piece
        return (
            piece_at_position is not None
            and piece_at_position.color != color
            and piece_at_position.type != PieceType.EMPTY
        )

    @staticmethod
    def is_king_in_check(color: Color, board: Dict[Tuple[int, int], Piece]) -> bool:
        """
        Check if the king of the given color is in check on the current board.

        Args:
            color (Color): The color of the king.
            board (Dict[Tuple[int, int], Piece]): The current state of the chessboard.

        Returns:
            bool: True if the king is in check, False otherwise.
        """

        # Find position of king in simulated position
        king_x, king_y = KingValidation.find_king_position(board, color)

        # Check for ray pieces in all directions
        ray_directions = [
            (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)
        ]

        knight_directions = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ]

        pawn_attack_directions = [
            (-1, -1),
            (-1, 1),  # For white king
            (1, -1),
            (1, 1),  # For black king
        ]

        for dx, dy in ray_directions:
            x, y = king_x + dx, king_y + dy

            while UniversalMovementValidation.is_within_board(x, y):
                if UniversalMovementValidation.is_not_occupied_by_allies(
                    board, x, y, color
                ):
                    piece_at_position = board.get((x, y))

                    # If it returns true, it can either be the opposing color or empty.
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

        # Check for knight attacks
        for dx, dy in knight_directions:
            x, y = king_x + dx, king_y + dy

            if UniversalMovementValidation.is_within_board(x, y):
                if UniversalMovementValidation.is_not_occupied_by_allies(
                    board, x, y, color
                ):
                    piece_at_position = board.get((x, y))

                    # If it returns true, it can either be the opposing color or empty.
                    if piece_at_position.type == PieceType.KNIGHT:
                        return True

        # Check for pawn attacks
        for dx, dy in pawn_attack_directions:
            x, y = king_x + dx, king_y + dy

            if UniversalMovementValidation.is_within_board(x, y):
                if UniversalMovementValidation.is_not_occupied_by_allies(
                    board, x, y, color
                ):
                    piece_at_position = board.get((x, y))

                    # If it returns true, it can either be the opposing color or empty.
                    if piece_at_position.type == PieceType.PAWN:
                        return True

        return False


PIECE_MOVE_MAP: Dict[PieceType, Type[PieceMovement]] = {
    PieceType.PAWN: PawnMovement,
    PieceType.ROOK: RookMovement,
    PieceType.BISHOP: BishopMovement,
    PieceType.QUEEN: QueenMovement,
    PieceType.KING: KingMovement,
    PieceType.KNIGHT: KnightMovement,
}
