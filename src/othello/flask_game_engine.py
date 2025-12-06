import tempfile
import json
import logging

from flask import Flask, render_template, request, jsonify, send_file
from flask.typing import ResponseReturnValue

from .components import (
    COLOUR_TYPE, BOARD_TYPE, initialise_board, make_move,
    invert_player_colour, player_can_move, find_winner
)
from .ai import get_ai_move
from .game_engine import BOARD_SIZE, MAX_MOVES, STARTING_PLAYER

RESPONSE_TYPE = dict[str, str | int | bool | COLOUR_TYPE | BOARD_TYPE]

# Create Logger
logger = logging.getLogger("othello_web")
logger.setLevel(logging.INFO)

# Add console handler to the logger
handler = logging.StreamHandler()
logging_format = "%(levelname)s:%(name)s:%(message)s"
handler.setFormatter(logging.Formatter(logging_format))
handler.setLevel(logging.INFO)
logger.addHandler(handler)

app = Flask(__name__, template_folder="../../templates")

class GameState:
    """Class to store information about the game state."""

    board: BOARD_TYPE
    current_player_colour: COLOUR_TYPE
    moves_left: int
    game_finished: bool
    game_mode: str

    def __init__(self, game_mode: str) -> None:
        """Initalise the game state for a given game mode."""
        self.board = initialise_board(size=BOARD_SIZE)
        self.current_player_colour = STARTING_PLAYER
        self.moves_left = MAX_MOVES
        self.game_finished = False
        self.game_mode = game_mode

    def update(self, data: RESPONSE_TYPE) -> None:
        """Update GameState values in place with given values."""
        for key, value in data.items():
            logger.info(f"Updating {key} from {getattr(self, key, value)} to {value}")
            setattr(self, key, value)

    def create_response(self, status: str, message: str="") -> RESPONSE_TYPE:
        """Create a response to send to the front-end."""
        return {
            "status": status,
            "message": message,
            "player": self.current_player_colour,
            "board": self.board,
            "finished": self.game_finished,
            "moves_left": self.moves_left,
            "game_mode": self.game_mode
        }

game_state = GameState("pvp")

@app.route("/", methods=["GET"])
def index() -> ResponseReturnValue:
    """Render the website, with a new PvP game."""
    global game_state
    game_state = GameState("pvp")

    logger.info("Rendered page.")

    return render_template("index.html", game_board=game_state.board)

@app.route("/newgame", methods=["GET"])
def new_game() -> ResponseReturnValue:
    """Begins a new game, with a game mode argument."""
    game_mode: str = request.args.get('game_mode').lower()
    status = "success"
    message = ""

    global game_state

    if game_mode not in ["ai", "pvp"]:
        status = "fail"
        message = "Failed to start new game. Game mode invalid."

        logger.error(message)
    else:
        game_state = GameState(game_mode)

        logger.info(f"Started new game. Mode: {game_mode}.")

    response = game_state.create_response(status, message)

    return jsonify(response)

@app.route("/download", methods=["GET"])
def download_game() -> ResponseReturnValue:
    """Return the game state as a JSON file."""
    global game_state

    # Use a tempfile
    temp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    )

    # Use the builtin __dict__ function to convert the game state object to JSON
    with temp:
        json.dump(game_state.__dict__, temp)

    logger.info("Sent the game state JSON.")

    return send_file(temp.name, as_attachment=True, download_name="game.json")

@app.route("/upload", methods=["POST"])
def upload_game() -> ResponseReturnValue:
    """Upload a given game state."""
    file = request.files.get("game_file")

    if file is None:
        message = "Failed to update game state. No file uploaded."
        logger.error(message)

        return jsonify({"status": "fail", "message": message})

    global game_state
    try:
        # restore JSON into your GameState
        game_state.update(json.load(file))

        logger.info("Updated game state.")

        response = game_state.create_response(status="success")

        return jsonify(response)
    except Exception as e:
        message = f"Failed to update game state. {str(e)}."

        return jsonify({"status": "fail", "message": message})

@app.route("/move", methods=["GET"])
def move() -> ResponseReturnValue:
    """Make a move on the board and check for a finished game. Optionally make an AI move."""
    global game_state

    status = "success"
    message = ""

    if game_state.game_finished:
        message = "Failed to make move. Game finished."
        logger.info(message)

        return jsonify({
            "status": "fail",
            "message": message
        })

    try:
        col = int(request.args.get("x")) - 1
        row = int(request.args.get("y")) - 1

        make_move(board=game_state.board, move=(row, col), colour=game_state.current_player_colour)
        logger.info(f"Made move: {(row, col)}.")

        game_state.moves_left -= 1

        # Determine next player after human move
        human_colour = game_state.current_player_colour
        next_colour = invert_player_colour(human_colour)

        # Check if the opponent can move
        if player_can_move(board=game_state.board, colour=next_colour):
            game_state.current_player_colour = next_colour
        else:
            message = f"Skipping {next_colour}'s turn."
            logger.info(message)

        # Check if the game mode is AI, and if it's the AI's turn and they have moves left
        if (game_state.game_mode == "ai" and
            game_state.current_player_colour != STARTING_PLAYER and
            game_state.moves_left > 0):

            ai_colour = game_state.current_player_colour

            # Generate an AI mode
            ai_move = get_ai_move(board=game_state.board, colour=ai_colour)

            # Check if the AI move is valid
            if ai_move is not None:
                make_move(board=game_state.board, move=ai_move, colour=ai_colour)

                logger.info(f"Made AI move: {ai_move}.")
            # If no move can be made, skip the AI's turn
            else:
                message = f"Skipping {ai_colour}'s turn."
                logger.info(message)

            game_state.moves_left -= 1

            # Check if the human can move
            if player_can_move(board=game_state.board, colour=human_colour):
                game_state.current_player_colour = human_colour
            else:
                message = f"Skipping {human_colour}'s turn."
                logger.info(message)

    except Exception as e:
        status = "fail"
        message = f"Failed to make move. {str(e)}"

        logger.error(message)

        return jsonify({
            "status": "fail",
            "message": message
        })

    # Check if board is full or neither player can move
    current_can_move = player_can_move(
        board=game_state.board,
        colour=game_state.current_player_colour
    )

    opponent_colour = invert_player_colour(game_state.current_player_colour)
    opponent_can_move = player_can_move(board=game_state.board, colour=opponent_colour)

    # If there is a winner, end the game and send the winner
    if game_state.moves_left <= 0 or (not current_can_move and not opponent_can_move):
        game_state.game_finished = True
        winner = find_winner(board=game_state.board)

        if winner is not None:
            message = f"{winner} won!"
        else:
            message = "Draw."

        logger.info(message)

    response = game_state.create_response(status, message)

    return jsonify(response)

if __name__ == "__main__":
    app.run()
    logger.info("Started othello-web.")
