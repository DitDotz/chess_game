from board import Board
from notation import Notation

if __name__ == "__main__":
    board = Board()
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    board.process_fen(starting_fen)
    print(board)

    # Gameloop
    while not board.king_in_checkmate:
        notation = Notation.get_valid_notation(board.board)
        board.move_piece(notation)
        print(board)

        if board.king_in_checkmate:
            print(f"{board.expected_player} is in checkmate")
            break


# reverse translator from grid to notation, and if invalid move is played, show valid_moves_list
# implement castling
