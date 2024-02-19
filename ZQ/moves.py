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

    # def get_special_moves(
    #     self, board: Dict[Tuple[int, int], Piece]
    # ) -> List[Tuple[int, int]]:
    #     return []


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
                and not UniversalMovementValidation.is_king_in_check()
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

    def get_special_moves(self, board: Dict[Tuple[int], Piece]) -> List[Tuple[int]]:
        # Implement castling king or queen side if the following conditions are fulfilled
        # queenside castling: empty squares between king and queen-rook, king and queen-rook has_moved=False and squares king must move through must not be attacked by any piece and cannot be in check
        # kingside castling: empty squares between king and king-rook, king and queen-rook has_moved=False and squares king must move through must not be attacked by any piece and cannot be in check
        pass


class KnightMovement(PieceMovement):
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
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
                    if UniversalMovementValidation.is_pinned_to_own_king(
                        originalPiece=self.piece, board=simulated_board
                    ):
                        break

                    valid_moves.append((dir_x, dir_y))

                break

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


class QueenMovement(PieceMovement):
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:

        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

        # Define directions for rook movement: up, down, left, right
        directions = [
            (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)
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


class PawnMovement(PieceMovement):
    def get_valid_moves(
        self, board: Dict[Tuple[int, int], Piece]
    ) -> List[Tuple[int, int]]:
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
            if not UniversalMovementValidation.is_pinned_to_own_king(
                self.piece, simulated_board
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
                        if not UniversalMovementValidation.is_pinned_to_own_king(
                            self.piece, simulated_board
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
                if not UniversalMovementValidation.is_pinned_to_own_king(
                    self.piece, simulated_board
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
                    and board[self.piece.x, self.piece.y + y].en_passantable == True
                ):
                    new_x, new_y = self.piece.x + direction, self.piece.y + y
                    # Simulate the move
                    simulated_board = deepcopy(board)
                    simulated_board[new_x, new_y] = self.piece
                    simulated_board[x, y] = Piece(
                        x, y, PieceType.EMPTY
                    )  # Update original position

                    # Check for pinning to own king
                    if not UniversalMovementValidation.is_pinned_to_own_king(
                        self.piece, simulated_board
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
                    and board[self.piece.x, self.piece.y + y].en_passantable == True
                ):
                    new_x, new_y = self.piece.x + direction, self.piece.y + y
                    # Simulate the move
                    simulated_board = deepcopy(board)
                    simulated_board[new_x, new_y] = self.piece
                    simulated_board[x, y] = Piece(
                        x, y, PieceType.EMPTY
                    )  # Update original position

                    # Check for pinning to own king
                    if not UniversalMovementValidation.is_pinned_to_own_king(
                        self.piece, simulated_board
                    ):

                        valid_moves.append((new_x, new_y))

        return valid_moves


class UniversalMovementValidation:
    @staticmethod
    def is_within_board(new_x: int, new_y: int) -> bool:
        return 0 <= new_x < 8 and 0 <= new_y < 8

    # Used on original board
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

    # board refers to simulated board
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

    # operated on simulated board (not sure if there is any difference)
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
