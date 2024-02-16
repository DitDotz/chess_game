from typing import Dict, Tuple, List
from pieces import Piece, PieceType, Color, FEN_MAP
from notation import Notation
from moves import PIECE_MOVE_MAP
from utility import BoardUtils


class Board:
    def __init__(self) -> None:
        self.board = self.empty_board()
        self.king_in_checkmate = False

    def empty_board(self) -> Dict[Tuple[int, int], Piece]:
        board: Dict[Tuple[int, int], Piece] = {}
        for x in range(8):
            for y in range(8):
                board[(x, y)] = Piece(x, y)
        return board

    # Need to implement an exception catch to input another fen
    # Does not specify whose turn it is, and if castling is still available
    def process_fen(self, fen: str) -> Dict[Tuple[int, int], Piece]:
        """
        Process the FEN string and return a dictionary containing the piece positions.
        """
        position_map: Dict[Tuple[int, int], str] = {}
        x, y = 0, 0

        for char in fen:
            if char == "/":
                x += 1
                y = 0
            elif char.isdigit():
                y += int(char)
            else:
                position_map[(x, y)] = char
                y += 1

        for x in range(x, 8):
            for y in range(y, 8):
                if (x, y) not in position_map:
                    position_map[(x, y)] = Piece(x, y)

        for position, fen_char in position_map.items():
            x, y = position
            piece = Piece(
                x,
                y,
                type=PieceType(FEN_MAP[fen_char.lower()]),
                color=Color.WHITE if fen_char.isupper() else Color.BLACK,
            )
            self.board[position] = piece

        return self.board

    def check_move_is_valid(self, notation: str) -> bool:
        original_pos, updated_piece = Notation.interpret_notation(notation)
        valid_moves = self.get_valid_moves(self.board[original_pos])
        return (updated_piece.x, updated_piece.y) in valid_moves

    def move_piece(self, notation: str) -> None:
        while True:
            if self.check_move_is_valid(notation):
                original_pos, updated_piece = Notation.interpret_notation(notation)
                self.board[original_pos] = Piece(
                    original_pos[0], original_pos[1], type=PieceType.EMPTY
                )
                new_x, new_y = updated_piece.x, updated_piece.y
                self.board[(new_x, new_y)] = updated_piece
                updated_piece.has_moved = True

                # Special check for double pawn moves
                if (
                    updated_piece.type == PieceType.PAWN
                    and abs(original_pos[0] - new_x) == 2
                ):
                    updated_piece.en_passantable = True
                else:
                    updated_piece.en_passantable = False

                # Special check for pawn promotion to queen
                self.board = BoardUtils.promote_pawn_if_available(
                    updated_piece, self.board
                )

                break
            else:
                print("Invalid move. Please try again.")
                notation = input("Enter notation: ")

    def get_valid_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """
        Get the valid moves for the given piece based on its type.
        """
        pieceMovement_class = PIECE_MOVE_MAP[piece.type]
        piece_movement_instance = pieceMovement_class(piece)
        if piece_movement_instance:
            return piece_movement_instance.get_valid_moves(self.board)
        else:
            print("Piece not recognized for movement")

    def __repr__(self) -> str:
        representation = "  a   b   c   d   e   f   g   h\n"  # Column labels

        for x in range(8):
            representation += (
                "|---" * 8 + "| " + str(8 - x) + "\n"
            )  # Add horizontal lines between rows and rank numbers

            for y in range(8):
                piece = self.board[(x, y)]
                representation += f"| {piece.repr} "  # Add piece representation

            representation += "|\n"  # End of row

        representation += (
            "|---" * 8 + "|\n"
        )  # Add horizontal lines for the bottom of the board
        representation += "  a   b   c   d   e   f   g   h\n"  # Column labels

        return representation
