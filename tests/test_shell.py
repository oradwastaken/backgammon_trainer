from backgammon import shell
from backgammon.board import Move


def test_parse_multiple_moves():
    assert len(shell.parse_moves("24/11")) == 1
    assert len(shell.parse_moves("24/11, 11/13")) == 2
    assert len(shell.parse_moves("24/11, 13/11, 11/5")) == 3


def test_parse_exact_moves():
    assert shell.parse_moves("24/11")[0] == Move(24, 11)
    assert shell.parse_moves("10/5") == [Move(10, 5)]
    assert shell.parse_moves("24/11, 5/1") == [Move(24, 11), Move(5, 1)]


def test_parse_moves_variations():
    assert shell.parse_moves("(13/8)") == [Move(13, 8)]
    assert shell.parse_moves("   (13/8)   ") == [Move(13, 8)]
    assert shell.parse_moves("(13/8") == [Move(13, 8)]
    assert shell.parse_moves("13/8") == [Move(13, 8)]
