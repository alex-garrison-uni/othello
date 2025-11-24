from othello.components import BOARD_TYPE, initialise_board

def get_board_with_moves(
        cell_assignments: list[tuple[int, int, str]],
        board_size: int = 8,
    ) -> BOARD_TYPE:
    """Set the given coordinates on the board to the given colour."""
    board = initialise_board(board_size)

    for row, col, colour in cell_assignments:
        board[row][col] = colour

    return board

def get_board_by_type(board_type: str, board_size: int = 8) -> BOARD_TYPE:
    """Return a board by a given type. Used for testing."""
    if board_type == "full_dark":
        return [["Dark" for _ in range(board_size)] for _ in range(board_size)]
    elif board_type == "full_light":
        return [["Light" for _ in range(board_size)] for _ in range(board_size)]
    elif board_type == "half_dark_half_light":
        board = [["Dark" for _ in range(board_size)] for _ in range(board_size)]

        for row in range(0, board_size // 2):
            board[row] = ["Light" for _ in range(board_size)]

        return board
