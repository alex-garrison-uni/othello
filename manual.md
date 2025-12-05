# Othello Manual

## Installation Instructions

1. Clone the repository:
```bash
git clone https://github.com/alex-garrison-uni/othello && cd othello
```

2. Install dependencies and package.
```bash
# With uv
uv sync # Use --no-dev for development enviroment
source .venv/bin/activate

# Using pip
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

3. Run the code

```bash
# Console
python3 -m othello.game_engine

# Start Flask back-end
python3 -m othello.flask_game_engine
```

## Running the web app
- Starting the Flask back-end will deploy the server on [http://127.0.0.1:5000](http://127.0.0.1:5000).
- The back-end only maintains one copy of the game state so the wen app cannot be used with multiple users.

## API Reference

### JSON
A standard JSON response format is used by the API to communicate the board state, or failures.

#### Success
```json
{
	status: "success",
	message: optional game detail
	board: 8x8 2D array contains "Dark", "Light" or null,
	finished: True if the game has finished,
	moves_left: remaining moves count,
	game_mode: "pvp" or "ai"
}
```

#### Failure
```json
{
	status: "fail",
	message: failure detail
}
```

### Routes

#### `GET /`
- Resets the server-side state to a new PvP game.
- Renders `templates/index.html`.

#### `GET /newgame`
- Starts a new game with a supplied mode.
- Arguments: `game_mode` (required, `"pvp"` or `"ai"`).
- [Failure](#failure) response if `game_mode` is not recognised.

#### `GET /download`
- Downloads the current game state as `game.json`.
- Response is an an attachment with the JSON file.

#### `POST /upload`
- Replaces the server-side game state with data from an uploaded JSON file.
- Request: `game_file` with JSON matching the download schema
- Responses:
	- [Success](#success) with the new game data
	- [Failure](#failure) if no file is uploaded, or the JSON schema is invalid.

#### `GET /move`
- Plays a move for the current player, in AI mode the AI may play immediately after.
- Arguments: `x` (column), `y` (row).
- If game is finished, returns [[#Failure]].
- Makes the human move, returning the new game state.
- If it is an AI game, it will also make an AI move.
- If the player does not have any legal moves, it will send a message saying their move has been skipped.
- If the game has been won/drawn, it will send `finished` as True, and the winner/draw as a message.
- Responses:
	- [Success](#success) with game state with move(s) made, and any skip/win/draw message.
	- [Failure](#failure) for invalid coordinates, illegal move, etc.

## Results

### Linting
```
uv run pylint src/othello/*

************* Module othello.ai
src/othello/ai.py:78:0: C0301: Line too long (109/100) (line-too-long)
src/othello/ai.py:79:0: C0301: Line too long (107/100) (line-too-long)
src/othello/ai.py:138:0: C0301: Line too long (106/100) (line-too-long)
src/othello/ai.py:141:0: C0301: Line too long (102/100) (line-too-long)
src/othello/ai.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module othello.components
src/othello/components.py:78:0: C0301: Line too long (105/100) (line-too-long)
src/othello/components.py:120:0: C0301: Line too long (109/100) (line-too-long)
src/othello/components.py:148:0: C0301: Line too long (109/100) (line-too-long)
src/othello/components.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/othello/components.py:3:0: C0103: Class name "COLOUR_TYPE" doesn't conform to PascalCase naming style (invalid-name)
src/othello/components.py:6:0: C0103: Class name "MOVE_TYPE" doesn't conform to PascalCase naming style (invalid-name)
src/othello/components.py:46:4: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
src/othello/components.py:79:8: W0612: Unused variable 'direction_name' (unused-variable)
src/othello/components.py:110:0: R0914: Too many local variables (16/15) (too-many-locals)
src/othello/components.py:112:4: R1720: Unnecessary "else" after "raise", remove the "else" and de-indent the code inside it (no-else-raise)
src/othello/components.py:122:12: W0612: Unused variable 'direction_name' (unused-variable)
src/othello/components.py:171:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
************* Module othello.flask_game_engine
src/othello/flask_game_engine.py:147:0: C0301: Line too long (109/100) (line-too-long)
src/othello/flask_game_engine.py:223:0: C0301: Line too long (103/100) (line-too-long)
src/othello/flask_game_engine.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/othello/flask_game_engine.py:15:0: C0103: Class name "RESPONSE_TYPE" doesn't conform to PascalCase naming style (invalid-name)
src/othello/flask_game_engine.py:23:0: C0103: Constant name "logging_format" doesn't conform to UPPER_CASE naming style (invalid-name)
src/othello/flask_game_engine.py:70:4: W0603: Using the global statement (global-statement)
src/othello/flask_game_engine.py:84:4: W0603: Using the global statement (global-statement)
src/othello/flask_game_engine.py:94:8: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
src/othello/flask_game_engine.py:103:4: W0602: Using global for 'game_state' but no assignment is done (global-variable-not-assigned)
src/othello/flask_game_engine.py:129:4: W0602: Using global for 'game_state' but no assignment is done (global-variable-not-assigned)
src/othello/flask_game_engine.py:140:11: W0718: Catching too general exception Exception (broad-exception-caught)
src/othello/flask_game_engine.py:148:4: W0602: Using global for 'game_state' but no assignment is done (global-variable-not-assigned)
src/othello/flask_game_engine.py:211:11: W0718: Catching too general exception Exception (broad-exception-caught)
src/othello/flask_game_engine.py:167:8: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
src/othello/flask_game_engine.py:196:16: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
src/othello/flask_game_engine.py:146:0: R0915: Too many statements (51/50) (too-many-statements)
************* Module othello.game_engine
src/othello/game_engine.py:118:0: C0301: Line too long (106/100) (line-too-long)
src/othello/game_engine.py:185:0: C0301: Line too long (106/100) (line-too-long)
src/othello/game_engine.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/othello/game_engine.py:31:8: W0707: Consider explicitly re-raising using 'except ValueError as exc' and 'raise ValueError('Coordinates must be integers.') from exc' (raise-missing-from)
src/othello/game_engine.py:54:15: W0718: Catching too general exception Exception (broad-exception-caught)
src/othello/game_engine.py:81:15: W0718: Catching too general exception Exception (broad-exception-caught)
src/othello/game_engine.py:124:8: R1723: Unnecessary "elif" after "break", remove the leading "el" from "elif" (no-else-break)
src/othello/game_engine.py:88:0: R0912: Too many branches (16/12) (too-many-branches)
src/othello/game_engine.py:207:20: R1720: Unnecessary "else" after "raise", remove the "else" and de-indent the code inside it (no-else-raise)
src/othello/game_engine.py:166:0: R0912: Too many branches (14/12) (too-many-branches)
------------------------------------------------------------------
Your code has been rated at 9.04/10 (previous run: 9.04/10, +0.00)
```

### Testing
```
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/alex/Library/CloudStorage/OneDrive-UniversityofExeter/Computer Science/Year 1/Programming/Coursework/Coursework 2/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/alex/Library/CloudStorage/OneDrive-UniversityofExeter/Computer Science/Year 1/Programming/Coursework/Coursework 2
configfile: pyproject.toml
testpaths: tests
collected 28 items

tests/test_ai.py::test_ai_outperforms_random_moves PASSED                                       [  3%]
tests/test_components.py::test_board_initialisation[4] PASSED                                   [  7%]
tests/test_components.py::test_board_initialisation[8] PASSED                                   [ 10%]
tests/test_components.py::test_board_initialisation[10] PASSED                                  [ 14%]
tests/test_components.py::test_zero_board_size_error PASSED                                     [ 17%]
tests/test_components.py::test_odd_board_size_error PASSED                                      [ 21%]
tests/test_components.py::test_legal_starting_moves[Dark-move0-True] PASSED                     [ 25%]
tests/test_components.py::test_legal_starting_moves[Dark-move1-False] PASSED                    [ 28%]
tests/test_components.py::test_legal_starting_moves[Light-move2-True] PASSED                    [ 32%]
tests/test_components.py::test_legal_starting_moves[Light-move3-False] PASSED                   [ 35%]
tests/test_components.py::test_legal_move_on_blocked_cell PASSED                                [ 39%]
tests/test_components.py::test_make_starting_moves[Dark-move0-expected0] PASSED                 [ 42%]
tests/test_components.py::test_make_starting_moves[Light-move1-expected1] PASSED                [ 46%]
tests/test_components.py::test_make_move PASSED                                                 [ 50%]
tests/test_components.py::test_invalid_move_error PASSED                                        [ 53%]
tests/test_components.py::test_find_winner[board0-None] PASSED                                  [ 57%]
tests/test_components.py::test_find_winner[board1-Dark] PASSED                                  [ 60%]
tests/test_components.py::test_find_winner[board2-Light] PASSED                                 [ 64%]
tests/test_components.py::test_find_winner[board3-None] PASSED                                  [ 67%]
tests/test_flask_game_engine.py::test_game_state_initialises_defaults[pvp] PASSED               [ 71%]
tests/test_flask_game_engine.py::test_game_state_initialises_defaults[ai] PASSED                [ 75%]
tests/test_flask_game_engine.py::test_update_overrides_state_values PASSED                      [ 78%]
tests/test_flask_game_engine.py::test_create_response_includes_current_state PASSED             [ 82%]
tests/test_game_engine.py::test_coords_input[2,1-expected0] PASSED                              [ 85%]
tests/test_game_engine.py::test_coords_input[8,8-expected1] PASSED                              [ 89%]
tests/test_game_engine.py::test_coords_input_error[abc,abc-coordinates must be integers] PASSED [ 92%]
tests/test_game_engine.py::test_coords_input_error[9,1-outside the board bounds] PASSED         [ 96%]
tests/test_game_engine.py::test_coords_input_error[1,2,3-two coordinates are required] PASSED   [100%]

28 passed in 3.54s
```

## Pre-commit
```
uv run pre-commit run --all-files

uv-lock..................................................................Passed
uv-export................................................................Passed
ruff check...............................................................Passed
ty check.................................................................Passed
pytest...................................................................Passed
```