"""
Module: notation.py

This module provides utilities for handling chess algebraic notation.
It includes functions for validating and interpreting chess notation.

Author: [Zhiquan]
Date: [02/21/2024]
"""

from typing import Tuple, Dict, List
from pieces import Piece, FEN_MAP, Color


class Notation:
    """
    A utility class for handling chess algebraic notation.

    This class provides methods to validate and interpret chess algebraic notation,
    ensuring that moves made on the board adhere to the rules of the game.

    """

    @staticmethod
    def get_valid_notation(board: Dict[Tuple[int, int], Piece]) -> str:
        """
        Prompt the user for valid chess algebraic notation.

        This method continuously prompts the user to enter valid chess algebraic notation
        until a valid move is provided based on the current board state.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chess board.

        Returns:
            str: A valid chess algebraic notation representing a legal move.

        """

        while True:
            notation = input("Enter notation: ")
            if Notation.notation_is_valid(board, notation):
                return notation
            else:
                print("Invalid move. Please try again.")

    @staticmethod
    def is_correct_format(notation: str) -> bool:
        """
        Check if the piece specified in the notation exists in the original position on the board.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chess board.
            notation (str): The chess algebraic notation representing the move.

        Returns:
            bool: True if the piece exists in the original position, False otherwise.

        """
        if len(notation) != 5:
            print("invalid notation format")
            return False  # Notation length should be exactly 5 characters

        if notation[0].lower() not in FEN_MAP.keys():
            print("invalid notation format")
            return False

        # Check if the positions are within the valid chess grid ('a1' to 'h8')
        if notation[1] not in "abcdefgh" or notation[2] not in "12345678":
            print("invalid notation format")
            return False

        if notation[3] not in "abcdefgh" or notation[4] not in "12345678":
            print("invalid notation format")
            return False

        return True

    @staticmethod
    def piece_exists_in_original_position(
        board: Dict[Tuple[int, int], Piece], notation: str
    ) -> bool:
        """
        Check if the piece specified in the notation exists in the original position on the board.
        """
        piece = notation[0]
        origin_row, origin_col = Notation.convert_to_coordinates(notation[1:3])
        color = Color.WHITE if notation[0].isupper() else Color.BLACK
        original_piece = board[(origin_row, origin_col)]

        if (
            original_piece.type != FEN_MAP[piece.lower()]
            or original_piece.color != color
        ):
            print(f"Piece {piece} does not exist at the specified position")
            return False  # Piece at original position does not match the specified piece in the notation

        return True

    @staticmethod
    def notation_is_valid(board: Dict[Tuple[int, int], Piece], notation: str) -> bool:
        """
        Check if the chess algebraic notation is valid.

        Args:
            board (Dict[Tuple[int, int], Piece]): The current state of the chess board.
            notation (str): The chess algebraic notation representing the move.

        Returns:
            bool: True if the notation is valid, False otherwise.

        """

        return (
            Notation.is_correct_format(notation)
            and Notation.piece_exists_in_original_position(board, notation)
            # Add other validation checks as needed...
        )

    @staticmethod
    def interpret_notation(notation: str) -> List:
        """
        Interpret chess algebraic notation and return the piece type, color, x, and y coordinates.

        Args:
            notation (str): The chess algebraic notation representing the move.

        Returns:
            List: A list containing the original position and the final piece after the move.

        """
        piece_type = FEN_MAP[(notation[0].lower())]
        piece_color = Color.WHITE if notation[0].isupper() else Color.BLACK
        original_pos = Notation.convert_to_coordinates(notation[1:3])
        final_pos = Notation.convert_to_coordinates(notation[3:5])
        final_pos_piece = Piece(
            x=final_pos[0], y=final_pos[1], type=piece_type, color=piece_color
        )

        return [original_pos, final_pos_piece]

    @staticmethod
    def convert_to_coordinates(chess_notation: str) -> Tuple[int, int]:
        """
        Convert algebraic chess notation to grid coordinates.

        Args:
            chess_notation (str): The algebraic chess notation to convert.

        Returns:
            Tuple[int, int]: A tuple containing the row and column coordinates.

        Raises:
            ValueError: If the input chess notation is invalid.

        """
        column_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        if len(chess_notation) != 2:
            raise ValueError("Invalid chess notation format")

        file_char, rank_char = chess_notation[0], chess_notation[1]
        if file_char not in column_map or not rank_char.isdigit():
            raise ValueError("Invalid chess notation format")

        # Convert rank to 0-indexed row, and adjust for Python indexing
        row = 8 - int(rank_char)
        column = column_map[file_char]

        return row, column
