import pytest

from othello.components import initialise_board, legal_move, make_move, find_winner
from testing_utils import get_board_with_assignments, get_board_by_type

@pytest.mark.parametrize("board_size", [4, 8, 10])
def test_board_initialisation(board_size):
    board = initialise_board(board_size)

    # Check the shape of the board is as expected
    assert len(board) == board_size
    assert all(len(row) == board_size for row in board)

    # Check that the expected starting positions are set
    upper_middle_index = int(board_size / 2)
    lower_middle_index = upper_middle_index - 1

    starting_positions = [
        board[lower_middle_index][lower_middle_index],
        board[lower_middle_index][upper_middle_index],
        board[upper_middle_index][lower_middle_index],
        board[upper_middle_index][upper_middle_index],
    ]

    assert starting_positions == ["Light", "Dark", "Dark", "Light"]

def test_zero_board_size_error():
    with pytest.raises(ValueError, match="Othello board size must be greater than 0."):
        initialise_board(0)

def test_odd_board_size_error():
    with pytest.raises(ValueError, match="Othello board size must be even."):
        initialise_board(7)

# Test legal move checking on horizonal and vertical axes
legal_starting_move_test_data = [
    ("Dark", (2, 3), True),
    ("Dark", (2, 4), False),
    ("Light", (2, 4), True),
    ("Light", (4, 5), False)
]
@pytest.mark.parametrize(("colour", "move", "expected"), legal_starting_move_test_data)
def test_legal_starting_moves(colour, move, expected):
    starting_board = initialise_board()

    assert legal_move(board=starting_board, move=move, colour=colour) == expected

def test_legal_move_on_blocked_cell():
    board = initialise_board()

    assert not legal_move(board=board, move=(3, 3), colour="Dark")

# Test move making on horizonal and vertical axes
make_starting_move_test_data = [
    (
        "Dark",
        (5, 4),
        get_board_with_assignments([(4, 4, "Dark"), (5, 4, "Dark")])
    ),
    (
        "Light",
        (3, 5),
        get_board_with_assignments([(3, 4, "Light"), (3, 5, "Light")])
    )
]
@pytest.mark.parametrize(("colour", "move", "expected"), make_starting_move_test_data)
def test_make_starting_moves(colour, move, expected):
    board = initialise_board()
    make_move(board=board, move=move, colour=colour)

    assert board == expected

# Test move making simultaneously on horizonal, vertical and diagonal axes
def test_make_move():
    board = get_board_with_assignments([
        (2, 2, "Light"),
        (2, 3, "Light"),
        (2, 4, "Light"),
        (3, 2, "Light"),
        (3, 3, "Light"),
        (3, 4, "Dark"),
        (3, 5, "Dark"),
        (4, 2, "Light"),
        (4, 3, "Light"),
        (4, 4, "Light")
    ])

    moves = [
        ((2, 3), "Dark"),
        ((2, 4), "Light"),
        ((3, 5), "Dark"),
        ((4, 2), "Light"),
        ((3, 2), "Dark"),
        ((2, 2), "Light")
    ]

    expected_board = initialise_board()

    for move, colour in moves:
        make_move(board=expected_board, move=move, colour=colour)

    assert board == expected_board

def test_invalid_move_error():
    starting_board = initialise_board()

    # Outside board bounds
    with pytest.raises(ValueError, match="Move is not legal."):
        make_move(board=starting_board, move=(-1, -1), colour="Dark")

    # Move on non-playable cell
    with pytest.raises(ValueError, match="Move is not legal."):
        make_move(board=starting_board, move=(1, 1), colour="Dark")

find_winner_test_data = [
    (initialise_board(), None),
    (get_board_by_type("full_dark"), "Dark"),
    (get_board_by_type("full_light"), "Light"),
    (get_board_by_type("half_dark_half_light"), None),
]
@pytest.mark.parametrize(("board", "expected"), find_winner_test_data)
def test_find_winner(board, expected):
    assert find_winner(board) == expected
