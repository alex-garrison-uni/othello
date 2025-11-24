import pytest
from othello.game_engine import parse_coords_input

@pytest.mark.parametrize("mock_input,expected", [("2,1", (1,0)), ("8,8", (7,7))])
def test_cli_coords_input(mock_input: str, expected: tuple[int]):
    assert parse_coords_input(mock_input) == expected

@pytest.mark.parametrize("mock_input", ["asdf", "9,1", "1,2,3"])
def test_cli_coords_input_error(mock_input: str):
    with pytest.raises(Exception):
        parse_coords_input(mock_input)
