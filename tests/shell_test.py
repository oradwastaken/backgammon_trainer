import pytest

from bgtrainer import shell
from bgtrainer.board import Move


@pytest.mark.parametrize(
    "test_input, expected_output", [("24/11", 1), ("24/11, 11/13", 2), ("24/11, 13/11, 11/5", 3)]
)
def test_parse_multiple_moves(test_input, expected_output):
    assert len(shell.parse_moves(test_input)) == expected_output


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        ("24/11, 5/1", [Move(24, 11), Move(5, 1)]),  # multiple moves
        ("13/8", [Move(13, 8)]),  # without brackets
        ("(13/8)", [Move(13, 8)]),  # with brackets
        ("(13/8", [Move(13, 8)]),  # only one bracket
        ("   (13/8)    ", [Move(13, 8)]),  # lots of white space
    ],
)
def test_parse_moves(test_input, expected_output):
    assert shell.parse_moves(test_input) == expected_output


# def test_parse_moves_errors():
#     assert shell.parse_moves("(138)") == []
