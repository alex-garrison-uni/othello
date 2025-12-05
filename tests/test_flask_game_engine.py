import pytest

from othello.components import initialise_board
from othello.flask_game_engine import GameState
from othello.game_engine import BOARD_SIZE, MAX_MOVES, STARTING_PLAYER
from testing_utils import get_board_with_assignments

@pytest.mark.parametrize("game_mode", ["pvp", "ai"])
def test_game_state_initialises_defaults(game_mode: str):
    game_state = GameState(game_mode)

    assert game_state.board == initialise_board(BOARD_SIZE)
    assert game_state.current_player_colour == STARTING_PLAYER
    assert game_state.moves_left == MAX_MOVES
    assert game_state.game_finished is False
    assert game_state.game_mode == game_mode

def test_update_overrides_state_values():
    game_state = GameState("pvp")
    updated_board = get_board_with_assignments(
        [(0, 0, "Dark"), (1, 1, "Light")], board_size=BOARD_SIZE
    )

    new_data = {
        "current_player_colour": "Light",
        "moves_left": 12,
        "game_finished": True,
        "board": updated_board,
        "game_mode": "ai",
    }

    game_state.update(new_data)

    assert game_state.current_player_colour == "Light"
    assert game_state.moves_left == 12
    assert game_state.game_finished is True
    assert game_state.board is updated_board
    assert game_state.game_mode == "ai"

def test_create_response_includes_current_state():
    game_state = GameState("ai")
    game_state.board = get_board_with_assignments([(3, 3, "Dark")], board_size=BOARD_SIZE)
    game_state.current_player_colour = "Light"
    game_state.moves_left = 3
    game_state.game_finished = True

    response = game_state.create_response(status="success", message="Board updated")

    assert response == {
        "status": "success",
        "message": "Board updated",
        "player": "Light",
        "board": game_state.board,
        "finished": True,
        "moves_left": 3,
        "game_mode": "ai",
    }
