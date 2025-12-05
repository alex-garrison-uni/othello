from othello.components import BOARD_TYPE, CELL_TYPE, initialise_board
from typing import Literal, cast

def get_board_with_assignments(
        cell_assignments: list[tuple[int, int, CELL_TYPE]],
        board_size: int = 8,
    ) -> BOARD_TYPE:
    """Set the given coordinates on the board to the given colour."""
    board = initialise_board(board_size)

    for row, col, colour in cell_assignments:
        board[row][col] = colour

    return board

def get_board_by_type(
        board_type: Literal["full_dark", "full_light", "half_dark_half_light"],
        board_size: int = 8
    ) -> BOARD_TYPE:
    """Return a board by a given type. Used for testing."""
    if board_type == "full_dark":
        return cast(BOARD_TYPE, [["Dark" for _ in range(board_size)] for _ in range(board_size)])
    elif board_type == "full_light":
        return cast(BOARD_TYPE, [["Light" for _ in range(board_size)] for _ in range(board_size)])
    elif board_type == "half_dark_half_light":
        board = [["Light" for _ in range(board_size)] for _ in range(board_size)]

        for row in range(0, board_size // 2):
            board[row] = ["Dark" for _ in range(board_size)]

        return cast(BOARD_TYPE, board)
