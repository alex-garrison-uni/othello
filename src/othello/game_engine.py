from .components import (
    MOVE_TYPE, initialise_board, print_board, make_move,
    find_winner, invert_player_colour, player_can_move,
    count_cells_for_colour
)
from .ai import get_ai_move

BOARD_SIZE = 8
MAX_MOVES = 60
STARTING_PLAYER = "Dark"

# Game Modes (in order)
# Player versus Player
# Player versus AI
PVP_MODE = 1
PVAI_MODE = 2

def parse_coords_input(coords_input: str) -> MOVE_TYPE:
    """Parse and return input board coordinates."""
    # Input has whitespace removed to allow for user error
    coords_clean_list: list[str] = [coord.strip() for coord in coords_input.strip().split(',')]

    # Check that the input has only two values
    if len(coords_clean_list) != 2:
        raise ValueError("Exactly two coordinates are required.")

    # Coords are converted to a 0-based indicies
    try:
        coord_row = int(coords_clean_list[0]) - 1
        coord_col = int(coords_clean_list[1]) - 1
    except ValueError:
        raise ValueError("Coordinates must be integers.")

    # Bounds check the input
    if not (0 <= coord_row < BOARD_SIZE and 0 <= coord_col < BOARD_SIZE):
        raise ValueError("Coordinates are outside the board bounds.")

    return (coord_row, coord_col)

def cli_coords_input() -> MOVE_TYPE:
    """Prompt user to input valid board coordinates."""
    valid_input = False

    # Continually wait for valid input
    while not valid_input:
        try:
            # Input should be two integers, comma-seperated
            user_input = input("Enter move: ")

            coords = parse_coords_input(user_input)

            valid_input = True

            continue
        except Exception:
            # Re-prompt the user
            print(f"Enter your move as two comma-seperated numbers between 1 and {BOARD_SIZE}")

    return coords

def game_mode_input() -> int:
    """Prompt user to input a valid game mode."""
    valid_input = False
    game_mode = None

    # Continually wait for valid input
    while not valid_input:
        try:
            # Input should be two integers, comma-seperated
            user_input = input("Please enter a game mode (PvP, AI): ")

            parsed_input = user_input.strip().lower()

            if parsed_input == "pvp":
                game_mode = PVP_MODE
                valid_input = True
            elif parsed_input == "ai":
                game_mode = PVAI_MODE
                valid_input = True

            continue
        except Exception:
            # Re-prompt the user
            continue

    return game_mode


def simple_game_loop() -> None:
    """Begin the CLI game loop."""
    print("""
    Welcome to Othello!

    Please enter your moves as two numbers between 1 and 8, comma-seperated.
    e.g. 3,4 makes a move on row 3 and column 4
    """)

    # Initalise game variables
    move_counter = MAX_MOVES
    board = initialise_board(BOARD_SIZE)
    current_player_colour = STARTING_PLAYER
    winner = None

    # Prompt the user for the game mode
    game_mode = game_mode_input()

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
        elif not current_player_can_move and opponent_can_move:
            print(f"Skipping {current_player_colour}'s turn.")
            current_player_colour = opponent_colour
        elif current_player_can_move:
            move_made = False

            print('')
            print_board(board)
            print(f"\n{current_player_colour}'s turn. {move_counter} moves left.")

            # Continually prompt the user for a valid, legal move
            while not move_made:
                if game_mode == PVP_MODE:
                    move = cli_coords_input()
                elif game_mode == PVAI_MODE:
                    if current_player_colour == "Dark":
                        move = cli_coords_input()
                    else:
                        move = get_ai_move(board=board, colour=current_player_colour)
                        print(f"AI move: {[i + 1 for i in move]}")

                try:
                    make_move(board=board, move=move, colour=current_player_colour)
                except ValueError as e:
                    print(e)
                else:
                    move_made = True

            # Once the move has been made, decrement the move counter and swap turns
            move_counter -= 1
            current_player_colour = opponent_colour

    # Find and print the winner
    winner = find_winner(board)

    if winner is not None:
        print(f"\n{winner} won!")
    else:
        print("\nDraw.")

    # Find and print the counter counts
    colour_counts = count_cells_for_colour(board)

    print(f"Dark: {colour_counts.get("Dark")} Light: {colour_counts.get("Light")}")

if __name__ == "__main__":
    simple_game_loop()
