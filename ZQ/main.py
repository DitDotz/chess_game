from board import Board
from notation import Notation
from moves import (
    RookMovement,
    BishopMovement,
    UniversalMovementValidation,
    QueenMovement,
    KnightMovement,
    PawnMovement,
    KingMovement,
)
from copy import deepcopy
from utility import BoardUtils
from pieces import FEN_MAP, Color

# clean up imports in the final stage
# if __name__ == "__main__":
# Infinite loop
board = Board()
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
board.process_fen(starting_fen)
print(board)

# Gameloop
while not board.king_in_checkmate:
    notation = Notation.get_valid_notation(board.board)
    board.move_piece(notation)
    print(board)

    if board.king_in_checkmate == True:
        print(f"{board.expected_player} is in checkmate")
        break


# reverse translator from grid to notation, and if invalid move is played, show valid_moves_list
# implement castling
# check_move_is_valid and get_valid_moves should be refactored
