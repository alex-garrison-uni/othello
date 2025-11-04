from typing import Optional

def initialise_board(size: int = 8) -> list[list[Optional[str]]]:
    """Return the Othello board."""
    if size % 2 != 0:
        raise ValueError("Othello board size must be even.")

    # Create the nested lists with a default value of None
    board = [[None for _ in range(size)] for _ in range(size)]

    # Dynamically generate indices for the middle of the board
    upper_middle_index = int(size / 2)
    lower_middle_index = upper_middle_index - 1

    # Set the starting position.
    board[lower_middle_index][lower_middle_index] = "Dark"
    board[lower_middle_index][upper_middle_index] = "Light"
    board[upper_middle_index][lower_middle_index] = "Light"
    board[upper_middle_index][upper_middle_index] = "Dark"

    return board

def print_board(board: list[list[Optional[str]]]):
    """Print a representation of the Othello board."""
    # Print the inital horizonal line
    print('―' * ((len(board) * 8) + 1))

    # For each cell, display it's value
    for row in range(0, len(board)):
        print('|', end='')

        for col in range(0, len(board)):
            if board[row][col]:
                print(' ' + board[row][col].ljust(6, ' '), end='|')
            else:
                print(' ' * 7, end='|')

        print('\n' + ('―' * ((len(board) * 8) + 1)))

def legal_move(board: list[list[Optional[str]]], move: tuple, colour: str) -> bool:
    """Return if a move is legal for a colour on a given Othello board."""
    opponent_colour = "Dark" if colour == "Light" else "Light"
    board_size = len(board)
    legal_move = True

    move_row, move_col = move

    # Generate slices of the board along the horizontal, vertical and primary and secondary diagonals
    horizonal_slice = board[move_row]
    vertical_slice = [board[row][move_col] for row in range(0, board_size)]

    c = move_col - move_row
    r0 = max(0, -c)
    r1 = min(board_size - 1, board_size - 1 - c)
    primary_diagonal_indices = [(r, r + c) for r in range(r0, r1 + 1)]
    primary_diagonal_slice = [board[row][col] for (row, col) in primary_diagonal_indices]
    primary_diagonal_move_index = move_row - r0

    s = move_row + move_col
    r0 = max(0, s - (board_size - 1))
    r1 = min(board_size - 1, s)
    secondary_diagonal_indices = [(r, s - r) for r in range(r0, r1 + 1)]
    secondary_diagonal_slice = [board[row][col] for (row, col) in secondary_diagonal_indices]
    secondary_diagonal_move_index = move_row - r0

    # Prepare each of the slices for traversion in both directions
    # Each slice is a list along an axis, beginning with the next cell after the proposed one
    traversable_slices = {
        "horizonal": {
            "forward": horizonal_slice[move_col+1:], 
            "backward": horizonal_slice[move_col-1:][::-1]
        },
        "vertical": {
            "forward": vertical_slice[move_row+1:], 
            "backward": vertical_slice[move_row-1:][::-1]
        },
        "primary_diagonal": {
            "forward": primary_diagonal_slice[primary_diagonal_move_index+1:], 
            "backward": primary_diagonal_slice[primary_diagonal_move_index-1:][::-1]
        },
        "secondary_diagonal": {
            "forward": secondary_diagonal_slice[secondary_diagonal_move_index+1:], 
            "backward": secondary_diagonal_slice[secondary_diagonal_move_index-1:][::-1]
        }
    }

    # For each axis, traverse along both directions
    # If a None cell is encountered, the move is not legal
    # If a cell is encountered for the player colour without encountering an opponent cell, the move is not legal
    # If a cell of the player colour is encountered after encountering ≥ 1 opponent cells, the move is legal
    for traversable_slice_name, traversable_slices in traversable_slices.items():
        for traversable_slice_direction, directed_traversable_slice in traversable_slices.items():
            encountered_opponent_colour = False

            for cell in directed_traversable_slice:
                if not cell:
                    legal_move = False
                    break
                elif cell == colour and not encountered_opponent_colour:
                    legal_move = False
                    break
                elif cell == colour and encountered_opponent_colour:
                    return legal_move
                elif cell == opponent_colour and not encountered_opponent_colour:
                    encountered_opponent_colour = True

    return legal_move