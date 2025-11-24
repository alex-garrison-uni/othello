from typing import Optional

DIRECTIONS = {
    "N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1),
    "NW": (-1, -1), "NE": (-1, 1), "SW": (1, -1), "SE": (1, 1)
}

BOARD_TYPE = list[list[Optional[str]]]

def initialise_board(size: int = 8) -> BOARD_TYPE:
    """Return the Othello board."""
    if size == 0:
        raise ValueError("Othello board size must be greater than 0.")
    if size % 2 != 0:
        raise ValueError("Othello board size must be even.")

    # Create the nested lists with a default value of None
    board = [[None for _ in range(size)] for _ in range(size)]

    # Dynamically generate indices for the middle of the board
    upper_middle_index = int(size / 2)
    lower_middle_index = upper_middle_index - 1

    # Set the starting position.
    board[lower_middle_index][lower_middle_index] = "Light"
    board[lower_middle_index][upper_middle_index] = "Dark"
    board[upper_middle_index][lower_middle_index] = "Dark"
    board[upper_middle_index][upper_middle_index] = "Light"

    return board

def print_board(board: BOARD_TYPE) -> None:
    """Print a representation of the Othello board."""
    # Print the column indicies
    print('    ', end='')
    for col_index in range(1, 9):
        print(str(col_index).center(8, ' '), end='')

    # Print the inital horizonal line
    print('\n   ' + ('―' * ((len(board) * 8) + 1)))

    # For each cell, display it's value
    for row in range(0, len(board)):
        # Print the row index
        print(f"{row+1}: |", end='')

        for col in range(0, len(board)):
            if board[row][col]:
                print(' ' + board[row][col].ljust(6, ' '), end='|')
            else:
                print(' ' * 7, end='|')

        print('\n   ' + ('―' * ((len(board) * 8) + 1)))

def invert_player_colour(colour: str) -> str:
    """Return the opposite player."""
    return "Dark" if colour == "Light" else "Light"

def legal_move(board: BOARD_TYPE, move: tuple, colour: str) -> bool:
    """Return if a move is legal for a colour on a given Othello board."""
    opponent_colour = invert_player_colour(colour)
    board_size = len(board)

    move_row, move_col = move

    if not (0 <= move_row < board_size and 0 <= move_col < board_size):
        raise ValueError("Move values must be between 0 and the board size.")

    # Check that the move cell is open
    if board[move_row][move_col]:
        return False

    # For each direction, traverse until you reach the end of the board, or find an illegal or legal move
    for direction_name, direction in DIRECTIONS.items():
        direction_row, direction_col = direction

        curr_row = move_row + direction_row
        curr_col = move_col + direction_col

        # The first step in the direction must encounter an opponent, and be on the board
        # If not, continue with the next direction
        if not (0 <= curr_row < board_size and 0 <= curr_col < board_size) or \
            board[curr_row][curr_col] != opponent_colour:
            continue

        # Continually step in the direction, until you reach the end of the board
        # or encounter something other than an opponent cell
        while (
            0 <= curr_row < board_size and
            0 <= curr_col < board_size and
            board[curr_row][curr_col] == opponent_colour
        ):
            curr_row = curr_row + direction_row
            curr_col = curr_col + direction_col

        # If the final cell to be traversed is the player colour and on the board, it is legal
        if (0 <= curr_row < board_size and
            0 <= curr_col < board_size and
            board[curr_row][curr_col] == colour
        ):
            return True

    return False

def make_move(board: BOARD_TYPE, move: tuple, colour: str) -> None:
    """Make a given move on the board."""
    if not legal_move(board=board, move=move, colour=colour):
        raise ValueError("Move is not legal.")
    else:
        opponent_colour = invert_player_colour(colour)
        board_size = len(board)

        move_row, move_col = move

        # For each direction, traverse until you reach the end of the board, or find an illegal or legal move
        # Store the coordinates of each cell traversed, and flip each one if the move is legal
        for direction_name, direction in DIRECTIONS.items():
            cell_indices_to_flip = [move]

            direction_row, direction_col = direction

            curr_row = move_row + direction_row
            curr_col = move_col + direction_col

            # The first step in the direction must encounter an opponent, and be on the board
            # If not, continue with the next direction
            if not (0 <= curr_row < board_size and 0 <= curr_col < board_size) or \
            board[curr_row][curr_col] != opponent_colour:
                continue

            # Continually step in the direction, until you reach the end of the board
            # or encounter something other than an opponent cell
            while (
                0 <= curr_row < board_size and
                0 <= curr_col < board_size and
                board[curr_row][curr_col] == opponent_colour
            ):
                cell_indices_to_flip.append((curr_row, curr_col))

                curr_row = curr_row + direction_row
                curr_col = curr_col + direction_col

            # If the final cell to be traversed is the player colour and on the board, the direction is legal
            # Flip each of the traversed cells for that direction
            if (0 <= curr_row < board_size and
                0 <= curr_col < board_size and
                board[curr_row][curr_col] == colour
            ):
                for row, col in cell_indices_to_flip:
                    board[row][col] = colour

def count_cells_for_colour(board: BOARD_TYPE) -> dict[str, int]:
    """Return a mapping of player colours to the amount of cells they have on a given board."""
    board_size = len(board)
    player_cell_count = {"Dark": 0, "Light": 0}

    for row in range(0, board_size):
        for col in range(0, board_size):
            if board[row][col] == "Dark":
                player_cell_count.update({"Dark": player_cell_count.get("Dark") + 1})
            elif board[row][col] == "Light":
                player_cell_count.update({"Light": player_cell_count.get("Light") + 1})

    return player_cell_count

def find_winner(board: BOARD_TYPE) -> Optional[str]:
    """Return the winner for a given board."""
    player_cell_count = count_cells_for_colour(board=board)

    if player_cell_count.get("Dark") > player_cell_count.get("Light"):
        return "Dark"
    if player_cell_count.get("Light") > player_cell_count.get("Dark"):
        return "Light"
    if player_cell_count.get("Dark") == player_cell_count.get("Light"):
        return None

def get_legal_moves(board: BOARD_TYPE, colour: str) -> list[tuple]:
    """Return a list of legal moves for a given board and colour."""
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

    return legal_moves

def player_can_move(board: BOARD_TYPE, colour: str) -> bool:
    """Return if a given player colour can move for a given board."""
    legal_moves_available_to_player = get_legal_moves(board=board, colour=colour)

    return len(legal_moves_available_to_player) > 0
