from typing import Optional
from .components import (
    initialise_board, print_board, make_move, 
    find_winner, invert_player_colour, player_can_move
)
from .ai import get_ai_move, get_random_move

BOARD_SIZE = 8
MAX_MOVES = 60
STARTING_PLAYER = "Dark"

# Game Modes (in order)
# Player versus Player
# Player versus AI
PVP_MODE = 1
PVAI_MODE = 2

def parse_coords_input(coords_input: str) -> tuple:
    """Parse and return input board coordinates."""
    # Input has whitespace removed to allow for user error, and is converted to a 0-based index
    coords = tuple(int(coord.strip()) - 1 for coord in coords_input.strip().split(','))

    # Check that the input has only two values
    assert len(coords) == 2

    # Bounds check the input
    coord_row, coord_col = coords
    if not (0 <= coord_row < BOARD_SIZE and 0 <= coord_col < BOARD_SIZE):
        raise ValueError()
    
    return coords

def cli_coords_input() -> tuple:
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
            print("Please enter your move as two numbers between 1 and 8, comma-seperated.")

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


def simple_game_loop():
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
                if not board[row][col]:
                    open_cell_indices.append((row, col))

        # Use the open cell indices to check if moves are available to the current player, or the opponent
        current_player_can_move = player_can_move(board=board, colour=current_player_colour)

        opponent_can_move = player_can_move(board=board, colour=current_player_colour)

        # If there are no legal moves left, exit the game loop
        if not current_player_can_move and not opponent_can_move:
            break
        # Skip the player's turn if they no move is available
        elif not current_player_can_move and opponent_can_move:
            print(f"Skipping {current_player_colour}'s turn.")
            current_player_colour = invert_player_colour(current_player_colour)
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
            current_player_colour = invert_player_colour(current_player_colour)

    winner = find_winner(board)

    if winner:
        print(f"\n{winner} won!")
    else:
        print("\nDraw.")

def ai_game_loop(random_moves: bool = False) -> Optional[str]:
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
                if not board[row][col]:
                    open_cell_indices.append((row, col))

        # Use the open cell indices to check if moves are available to the current player, or the opponent
        current_player_can_move = player_can_move(board=board, colour=current_player_colour)

        opponent_can_move = player_can_move(board=board, colour=current_player_colour)

        # If there are no legal moves left, exit the game loop
        if not current_player_can_move and not opponent_can_move:
            break
        # Skip the player's turn if they no move is available
        elif not current_player_can_move and opponent_can_move:
            current_player_colour = invert_player_colour(current_player_colour)
        elif current_player_can_move:
            move_made = False

            # Get move (either AI generated, or random)
            while not move_made:
                if random_moves and current_player_colour is STARTING_PLAYER:
                    move = get_random_move(board=board, colour=current_player_colour)
                else:
                    move = get_ai_move(board=board, colour=current_player_colour)

                try:
                    make_move(board=board, move=move, colour=current_player_colour)
                except ValueError as e:
                    raise e
                else:
                    move_made = True

            # Once the move has been made, decrement the move counter and swap turns
            move_counter -= 1
            current_player_colour = invert_player_colour(current_player_colour)

    return find_winner(board)

if __name__ == "__main__":
    ai_game_loop(random_moves=False)