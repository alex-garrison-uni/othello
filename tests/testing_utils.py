from othello.components import (
    BOARD_TYPE, CELL_TYPE, initialise_board,
    find_winner, make_move, invert_player_colour, player_can_move
)
from othello.game_engine import MAX_MOVES, STARTING_PLAYER, BOARD_SIZE
from othello.ai import get_random_move, get_ai_move
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

def ai_game_loop(random_moves: bool = False) -> str | None:
    """Begin the AI game loop and return the winner."""
    # Initalise game variables
    move_counter = MAX_MOVES
    board = initialise_board(BOARD_SIZE)
    current_player_colour = STARTING_PLAYER

    # Continue the game loop until either one player wins, or the move counter runs out
    while move_counter > 0:
        # Find the indices of all open cells
        open_cell_indices = []

        for row in range(0, BOARD_SIZE):
            for col in range(0, BOARD_SIZE):
                if board[row][col] is None:
                    open_cell_indices.append((row, col))

        opponent_colour = invert_player_colour(current_player_colour)

        # Use the open cell indices to check if moves are available to any player
        current_player_can_move = player_can_move(board=board, colour=current_player_colour)

        opponent_can_move = player_can_move(board=board, colour=opponent_colour)

        # If there are no legal moves left, exit the game loop
        if not current_player_can_move and not opponent_can_move:
            break
        # Skip the player's turn if they no move is available
        if not current_player_can_move and opponent_can_move:
            current_player_colour = opponent_colour
        elif current_player_can_move:
            move_made = False

            # Get move (either AI generated, or random)
            while not move_made:
                if random_moves and current_player_colour is STARTING_PLAYER:
                    move = get_random_move(board=board, colour=current_player_colour)
                else:
                    move = get_ai_move(board=board, colour=current_player_colour)

                if move is not None:
                    try:
                        make_move(board=board, move=move, colour=current_player_colour)
                    except ValueError as e:
                        raise e
                    else:
                        move_made = True
                else:
                    raise RuntimeError("Failed to generated AI move.")

            # Once the move has been made, decrement the move counter and swap turns
            move_counter -= 1
            current_player_colour = opponent_colour

    return find_winner(board)
