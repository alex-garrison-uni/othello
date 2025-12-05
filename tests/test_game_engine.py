import pytest
import re
from othello.game_engine import parse_coords_input

@pytest.mark.parametrize(("mock_input", "expected"), [("2,1", (1,0)), ("8,8", (7,7))])
def test_coords_input(mock_input: str, expected: tuple[int]):
    assert parse_coords_input(mock_input) == expected

@pytest.mark.parametrize(
    ("mock_input", "expected_error_regex"), [
        ("abc,abc", "coordinates must be integers"),
        ("9,1", "outside the board bounds"),
        ("1,2,3", "two coordinates are required")
])
def test_coords_input_error(mock_input: str, expected_error_regex: str):
    with pytest.raises(
        expected_exception=ValueError,
        # Case-insensitive regex matching for error messages
        match=re.compile(expected_error_regex, re.IGNORECASE)
    ):
        parse_coords_input(mock_input)
