import tempfile
import json
from flask import Flask, render_template, request, jsonify, send_file
from .components import (
    initialise_board, make_move, invert_player_colour,
    player_can_move, find_winner, BOARD_TYPE
)
from .ai import get_ai_move
from .game_engine import BOARD_SIZE, MAX_MOVES, STARTING_PLAYER

app = Flask(__name__, template_folder="../../templates")

class GameState:
    """Class to store information about the game state."""

    board: BOARD_TYPE
    current_player_colour: str
    moves_left: int
    game_finished: bool
    game_mode: str

    def __init__(self, game_mode):
        """Initalise the game state for a given game mode."""
        self.board = initialise_board(size=BOARD_SIZE)
        self.current_player_colour = STARTING_PLAYER
        self.moves_left = MAX_MOVES
        self.game_finished = False
        self.game_mode = game_mode

    def update(self, data):
        """Update object values."""
        for key, value in data.items():
            print(f"Updating {key} from {getattr(self, key, value)} to {value}")
            setattr(self, key, value)

    def create_response(self, status, message=None):
        """Create a response to send to the front-end."""
        return {
            "status": status,
            "message": message,
            "player": self.current_player_colour,
            "board": self.board,
            "finished": self.game_finished,
            "moves_left": self.moves_left,
            "game_mode": "pvp" if self.game_mode == "pvp" else "ai"
        }

game_state = GameState("pvp")

@app.route("/", methods=["GET"])
def index():
    """Render the website, with a new PvP game."""
    global game_state
    game_state = GameState("pvp")
    return render_template("index.html", game_board=game_state.board)

@app.route("/newgame", methods=["GET"])
def new_game():
    """Begins a new game, with a game mode argument."""
    game_mode = request.args.get('game_mode').lower()
    status = "success"
    message = None

    global game_state

    if game_mode not in ["ai", "pvp"]:
        status = "fail"
        message = "Game mode invalid."
    else:
        game_state = GameState(game_mode)

    response = game_state.create_response(status, message)

    return jsonify(response)

@app.route("/download", methods=["GET"])
def download_game():
    """Return the game state as a JSON file."""
    global game_state

    # Use a tempfile
    temp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    )

    # Use the builtin __dict__ function to convert the game state object to JSON
    with temp:
        json.dump(game_state.__dict__, temp)

    return send_file(temp.name, as_attachment=True, download_name="game.json")

@app.route("/upload", methods=["POST"])
def upload_game():
    """Upload a given game state."""
    file = request.files.get("game_file")

    if not file:
        return jsonify({"status": "fail", "message": "No file uploaded"}), 400

    global game_state
    try:
        # restore JSON into your GameState
        game_state.update(json.load(file))

        response = game_state.create_response(status="success")

        return jsonify(response)

    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})

@app.route("/move", methods=["GET"])
def move():
    """Make a move on the board and check for a finished game. If is is the AI game mode, make an AI move."""
    col = int(request.args.get("x")) - 1
    row = int(request.args.get("y")) - 1

    global game_state

    status = "success"
    message = None

    if game_state.game_finished:
        return jsonify({
            "status": "fail",
            "message": "Game finished."
        })

    try:
        make_move(board=game_state.board, move=(row, col), colour=game_state.current_player_colour)

        game_state.moves_left -= 1

        # Determine next player after human move
        human_colour = game_state.current_player_colour
        next_colour = invert_player_colour(human_colour)

        # Check if the opponent can move
        if player_can_move(board=game_state.board, colour=next_colour):
            game_state.current_player_colour = next_colour
        else:
            message = f"Skipping {next_colour}'s turn."

        # Check if the game mode is AI, and if it's the AI's turn and they have moves left
        if (game_state.game_mode == "ai" and
            game_state.current_player_colour != STARTING_PLAYER and
            game_state.moves_left > 0):

            ai_colour = game_state.current_player_colour

            # AI makes its move
            ai_move = get_ai_move(board=game_state.board, colour=ai_colour)
            make_move(board=game_state.board, move=ai_move, colour=ai_colour)

            game_state.moves_left -= 1

            # Check if the human can move
            if player_can_move(board=game_state.board, colour=human_colour):
                game_state.current_player_colour = human_colour
            else:
                message = f"Skipping {human_colour}'s turn."

    except Exception as e:
        status = "fail"
        message = str(e)

    # Check if board is full or neither player can move
    current_can_move = player_can_move(board=game_state.board, colour=game_state.current_player_colour)
    opponent_colour = invert_player_colour(game_state.current_player_colour)
    opponent_can_move = player_can_move(board=game_state.board, colour=opponent_colour)

    if game_state.moves_left <= 0 or (not current_can_move and not opponent_can_move):
        game_state.game_finished = True
        winner = find_winner(board=game_state.board)
        if winner:
            message = f"{winner} won!"
        else:
            message = "Draw."

    response = game_state.create_response(status, message)

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
