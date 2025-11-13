import copy
import random
import math
from .components import (
    BOARD_TYPE, get_legal_moves, 
    make_move, invert_player_colour
)

CORNER_WEIGHT = 30
EDGE_WEIGHT = 15
CORNER_ADJ_WEIGHT = 20
EDGE_ADJ_WEIGHT = 10
CORNER_ADJ_ADJ_WEIGHT = 6
EDGE_ADJ_ADJ_WEIGHT = 1

def get_random_move(board: BOARD_TYPE, colour: str) -> tuple[int, int]:
    """Return a random move for a given board and colour."""
    legal_moves = get_legal_moves(board=board, colour=colour)

    if len(legal_moves) == 0:
        return None
    else:
        return random.choice(legal_moves)

def get_ai_move(board: BOARD_TYPE, colour: str) -> tuple[int, int]:
    """Return a AI generated move for a given board and colour."""
    potential_board_states = get_potential_board_states(board=board, colour=colour)

    best_scoring_move = None
    highest_board_score = -math.inf
    for move, potential_board_state in potential_board_states.items():
        potential_board_score = score_board(board=potential_board_state, colour=colour)

        if potential_board_score > highest_board_score:
            highest_board_score = potential_board_score
            best_scoring_move = move

    return best_scoring_move

def score_board(board: BOARD_TYPE, colour: str) -> int:
    """Return a score for a given board and colour between -200 to 200."""
    opponent_colour = invert_player_colour(colour)
    score = 0

    moves_available = len(get_legal_moves(board=board, colour=colour))
    opponent_moves_available = len(get_legal_moves(board=board, colour=opponent_colour))

    if moves_available == 0  and opponent_moves_available == 0:
        score -= 5
    elif moves_available == 0:
        score -= 10
    elif opponent_moves_available == 0:
        score += 15
    else:
        score += max(moves_available - opponent_moves_available, 10)

    board_position_metrics = get_board_position_metrics(board=board)
    player_metrics = board_position_metrics.get(colour)

    player_score = (
        player_metrics.get("corner") * CORNER_WEIGHT
        + player_metrics.get("edge") * EDGE_WEIGHT
        - player_metrics.get("corner_adj") * CORNER_ADJ_WEIGHT
        - player_metrics.get("edge_adj") * EDGE_ADJ_WEIGHT
        + player_metrics.get("corner_adj_adj") * CORNER_ADJ_ADJ_WEIGHT
        + player_metrics.get("edge_adj_adj") * EDGE_ADJ_ADJ_WEIGHT
    )

    score += player_score

    return score

def get_potential_board_states(board: BOARD_TYPE, colour: str) -> dict[tuple[int, int], BOARD_TYPE]:
    """Return a mapping of potential moves to board states from a given board state, for a given colour."""
    legal_moves = get_legal_moves(board=board, colour=colour)

    if len(legal_moves) == 0:
        return None
    
    potential_board_states = {}
    for legal_move in legal_moves:
        potential_board_state = copy.deepcopy(board)

        make_move(board=potential_board_state, move=legal_move, colour=colour)

        potential_board_states[legal_move] = potential_board_state

    return potential_board_states

def get_board_position_metrics(board: BOARD_TYPE):
    """Return metrics about the count of cells positioned around the board, by colour."""
    board_size = len(board)

    metrics = {
        "corner": 0, "edge": 0, 
        "corner_adj": 0, "edge_adj": 0,
        "corner_adj_adj": 0, "edge_adj_adj": 0
    }
    board_position_metrics = {
        "Dark": copy.deepcopy(metrics), 
        "Light": copy.deepcopy(metrics)
    }

    edge_indices = [0, board_size-1]
    edge_adj_indices = [1, board_size-2]
    edge_adj_adj_indices = [2, board_size-3]


    for row in range(board_size):
        for col in range(board_size):
            cell = board[row][col]
            
            if cell:
                cell_metrics = board_position_metrics.get(board[row][col])

                # Check for corner cells
                if row in edge_indices and col in edge_indices:
                    cell_metrics.update({"corner": cell_metrics.get("corner") + 1})
                # Check for edge cells
                elif (row in edge_indices and col not in edge_adj_indices) or \
                    (col in edge_indices and row not in edge_adj_indices):
                    cell_metrics.update({"edge": cell_metrics.get("edge") + 1})
                # Check for corner adjacent cells
                elif row in edge_adj_indices and col in edge_adj_indices:
                    cell_metrics.update({"corner_adj": cell_metrics.get("corner_adj") + 1})
                # Check for edge adjacent cells
                elif row in edge_adj_indices or col in edge_adj_indices:
                    cell_metrics.update({"edge_adj": cell_metrics.get("edge_adj") + 1})
                # Check for corner adjacent adjacent cells
                elif row in edge_adj_adj_indices and col in edge_adj_adj_indices:
                    cell_metrics.update({"corner_adj_adj": cell_metrics.get("corner_adj_adj") + 1})
                # Check for edge adjacent adjacent cells
                elif row in edge_adj_adj_indices or col in edge_adj_adj_indices:
                    cell_metrics.update({"edge_adj_adj": cell_metrics.get("edge_adj_adj") + 1})
    
    return board_position_metrics