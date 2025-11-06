from .components import (
    initialise_board, print_board, legal_move, 
    make_move, find_winner, invert_player_colour
)

BOARD_SIZE = 8

def get_board_with_moves(
        cell_assignments: list[tuple[int, int, str]],
        board_size: int = 8,
    ):
    """Set the given coordinates on the board to the given colour."""
    board = initialise_board(board_size)

    for row, col, colour in cell_assignments:
        board[row][col] = colour

    return board

def cli_coords_input() -> tuple:
    """Return user-input board coordinates."""
    valid_input = False

    # Continually prompt user for a valid move
    while not valid_input:
        try:
            # Moves should be entered as two integers, comma-seperated
            raw_input = input("Enter move: ")

            # Input has whitespace removed to allow for user error, and is converted to a 0-based index
            coords = tuple(int(coord.strip()) - 1 for coord in raw_input.strip().split(','))

            # Check that the input has only two values
            assert len(coords) == 2

            # Bounds check the input
            coord_row, coord_col = coords
            if not (0 <= coord_row < BOARD_SIZE and 0 <= coord_col < BOARD_SIZE):
                raise ValueError()

            valid_input = True

            continue
        except Exception:
            print("Please enter your move as two numbers between 1 and 8, comma-seperated.")

    return coords

def simple_game_loop():
    """Begin the CLI game loop."""
    print("""
    Welcome to Othello!

    Please enter your moves as two numbers between 1 and 8, comma-seperated.
    e.g. 3,4 makes a move on row 3 and column 4
    """)

    # Initalise game variables
    move_counter = 60
    board = initialise_board(BOARD_SIZE)
    current_player_colour = "Dark"
    winner = None

    # Continue the game loop until either one player wins, or the move counter runs out
    while move_counter > 0:
        # Find the indices of all open cells
        open_cell_indices = []

        for row in range(0, BOARD_SIZE):
            for col in range(0, BOARD_SIZE):
                if not board[row][col]:
                    open_cell_indices.append((row, col))

        # Use the open cell indices to check if moves are available to the current player, or the opponent
        legal_move_available_to_player = any(
            legal_move(board=board, move=open_cell_index, colour=current_player_colour) 
            for open_cell_index in open_cell_indices
        )

        legal_move_available_to_opponent = any(
            legal_move(board=board, move=open_cell_index, colour=invert_player_colour(current_player_colour)) 
            for open_cell_index in open_cell_indices
        )

        # If there are no legal moves left, exit the game loop
        if not legal_move_available_to_player and not legal_move_available_to_opponent:
            break
        # Skip the player's turn if they no move is available
        elif not legal_move_available_to_player and legal_move_available_to_opponent:
            print(f"Skipping {current_player_colour}'s turn.")
            current_player_colour = invert_player_colour(current_player_colour)
        elif legal_move_available_to_player:
            move_made = False

            print('')
            print_board(board)
            print(f"\n{current_player_colour}'s turn. {move_counter} moves left.")

            # Continually prompt the user for a valid, legal move
            while not move_made:
                move = cli_coords_input()

                try:
                    make_move(board=board, move=move, colour=current_player_colour)
                except ValueError as e:
                    print(e)
                else:
                    move_made = True
            
            # Once the move has been made, decrement the move counter and swap turns
            move_counter -= 1
            current_player_colour = invert_player_colour(current_player_colour)
    
    winner = find_winner(board)

    if winner:
        print(f"\n{winner} won!")
    else:
        print("\nDraw.")

if __name__ == "__main__":
    simple_game_loop()