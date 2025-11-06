from typing import Optional
import random
from othello.components import initialise_board, legal_move

def get_board_with_moves(
        cell_assignments: list[tuple[int, int, str]],
        board_size: int = 8,
    ) -> list[list[Optional[str]]]:
    """Set the given coordinates on the board to the given colour."""
    board = initialise_board(board_size)

    for row, col, colour in cell_assignments:
        board[row][col] = colour

    return board

def get_board_by_type(board_type: str, board_size: int = 8) -> list[list[Optional[str]]]:
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

def get_random_move(board: list[list[Optional[str]]], colour: str) -> tuple:
    board_size = len(board)

    open_cell_indices = []

    for row in range(0, board_size):
        for col in range(0, board_size):
            if not board[row][col]:
                open_cell_indices.append((row, col))

    legal_moves = []

    for open_cell_index in open_cell_indices:
        is_legal = legal_move(board=board, move=open_cell_index, colour=colour) 

        if is_legal:
            legal_moves.append(open_cell_index)

    return random.choice(legal_moves)