from typing import Dict, Tuple
from pieces import *
from notation import *


class Board:
    def __init__(self) -> None:
        self.board = self.empty_board()

    def empty_board(self) -> Dict[Tuple[int, int], Piece]:
        board: Dict[Tuple[int, int], Piece] = {}
        for x in range(8):
            for y in range(8):
                board[(x, y)] = Piece(x, y)
        return board

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

    def move_piece(self, piece: Piece, fen_notation: str) -> None:
        """
        Move a piece to a new position on the board, disregarding valid moves.
        Replace the original position with an empty piece.
        TODO change function such that it doesn't require input position
        """
        # Replace the original position with an empty piece
        self.board[(piece.x, piece.y)] = Piece(piece.x, piece.y)

        # create new piece based on notation

        new_piece = interpret_notation(fen_notation)

        # Place the piece at the new position
        self.board[(new_piece.x, new_piece.y)] = new_piece

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


board = Board()
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
board.process_fen(starting_fen)

print(board)
