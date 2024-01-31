from typing import Dict, Tuple

Position = Tuple[int, int]


def process_fen(fen: str) -> Dict[Position, str]:
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

    return position_map


starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


map = process_fen(starting_fen)
print(map)
