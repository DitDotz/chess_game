class PieceMovement(ABC):
    def __init__(self, piece: Piece):
        self.piece = piece

    @abstractmethod
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
        pass


# Not fully implemented
# is_king_in_check_after_move
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
                and not UniversalMovementValidation.is_king_in_check_after_move()
            ):
                valid_moves.append((new_x, new_y))

        return valid_moves


class RookMovement(PieceMovement):
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color
        new_x, new_y = None, None  # to edit

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
        new_x, new_y = None, None  # to edit

        return valid_moves


class BishopMovement(PieceMovement):
    def get_valid_moves(self, board: List[List[Piece]]) -> List[Tuple[int, int]]:
        valid_moves = []
        x, y = self.piece.x, self.piece.y
        color = self.piece.color

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
        direction = 1 if color == Color.WHITE else -1

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

        return (
            piece_at_position.color != color
            or piece_at_position.type == PieceType.EMPTY
        )

    @staticmethod
    def not_pinned_by_king():
        pass

    @staticmethod
    def is_king_in_check_after_move():
        pass

    @staticmethod
    def is_occupied_by_opposing(
        board: List[List[Piece]], new_x: int, new_y: int, color: Color
    ) -> bool:
        """
        Check if the square at the given coordinates is occupied by an opposing piece.
        """
        if not UniversalMovementValidation.is_within_board(new_x, new_y):
            return False

        piece_at_position = board[(new_x, new_y)]

        # Check if the square is occupied by an opposing piece
        return (
            piece_at_position.color != color
            and piece_at_position.type != PieceType.EMPTY
        )
