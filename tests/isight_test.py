import pytest

from bgtrainer.board import Board, iSight, Team


def test_iSight__empty_board_is_0():
    assert iSight(Board()) == 0


def test_iSight__more_pips_for_more_checkers():
    """Add 1 pip for each additional checker on the board compared to the opponent;"""
    board = Board()
    board.points[1].num_checkers = 2
    board.points[1].color = Team.X

    board.points[24].num_checkers = 1
    board.points[24].color = Team.O

    # Your pip count is 2, and you add 1 because you have an additional checker:
    assert iSight(board) == 3

    board = Board()
    board.points[1].num_checkers = 2
    board.points[1].color = Team.X
    board.points[2].num_checkers = 2
    board.points[2].color = Team.X

    board.points[24].num_checkers = 1
    board.points[24].color = Team.O

    # Your pip count is 6, and you add 3 because you have 3 additional checkers:
    assert iSight(board) == 9

    board = Board()
    board.points[1].num_checkers = 1
    board.points[1].color = Team.X

    board.points[24].num_checkers = 1
    board.points[24].color = Team.O

    # Your pip count is 2, and you add nothing because you have the same number of checkers:
    assert iSight(board) == 1


@pytest.mark.parametrize(
    "num_checkers, expected_isight",
    [
        (2, 2),  # Your pip count is 2, and you add nothing because you just have 2 checkers
        (3, 5),  # Your pip count is 3, and you add 2 for having 2+1 checkers on point 1
        (4, 8),  # Your pip count is 4, and you add 4 for having 2+2 checkers on point 1
    ],
)
def test_iSight__more_pips_for_more_checkers_point_1(num_checkers, expected_isight):
    """Add 2 pips for each checker more than 2 on point 1;"""
    board = Board()
    board.points[1].num_checkers = num_checkers
    board.points[1].color = Team.X

    board.points[24].num_checkers = num_checkers
    board.points[24].color = Team.O

    assert iSight(board) == expected_isight


@pytest.mark.parametrize(
    "num_checkers, expected_isight",
    [
        (2, 4),  # Your pip count is 4, and you add nothing because you just have 2 checkers
        (3, 8),  # Your pip count is 6, and you add 2 for having 2+1 checkers on point 2
        (4, 12),  # Your pip count is 8, and you add 4 for having 2+2 checkers on point 2
    ],
)
def test_iSight__more_pips_for_more_checkers_point_2(num_checkers, expected_isight):
    """Add 1 pip for each checker more than 2 on point 2;"""
    board = Board()
    board.points[2].num_checkers = num_checkers
    board.points[2].color = Team.X

    board.points[23].num_checkers = num_checkers
    board.points[23].color = Team.O

    assert iSight(board) == expected_isight


@pytest.mark.parametrize(
    "num_checkers, expected_isight",
    [
        (3, 8),  # Your pip count is 9, and you add nothing because you just have 3 checkers
        (4, 12),  # Your pip count is 12, and you add 1 for having 3+1 checkers on point 2
        (5, 4),  # Your pip count is 15, and you add 2 for having 3+1 checkers on point 2
    ],
)
def test_iSight__more_pips_for_more_checkers_point_3(num_checkers, expected_isight):
    """Add 1 pip for each checker more than 3 on point 3;"""
    board = Board()
    board.points[3].num_checkers = num_checkers
    board.points[3].color = Team.X

    board.points[22].num_checkers = num_checkers
    board.points[22].color = Team.O

    assert iSight(board) == expected_isight


@pytest.mark.parametrize(
    "point_num, expected_isight",
    [
        (4, 1),  # add 1
        (5, 1),  # add 1
        (6, 1),  # add 1
    ],
)
def test_iSight__more_pips_for_gaps(point_num, expected_isight):
    """Add 1 pip for each empty space on points 4, 5, or 6 (only if the other player has
    a checker on his corresponding point);"""
    board = Board()
    board.points[25 - point_num].num_checkers = 1
    board.points[25 - point_num].color = Team.O
    assert iSight(board) == expected_isight


@pytest.mark.parametrize(
    "point_num, expected_isight",
    [
        (4, 4),  # Your pip count is 4, and you don't add anything
        (5, 5),  # Your pip count is 5, and you don't add anything
        (6, 6),  # Your pip count is 6, and you don't add anything
    ],
)
def test_iSight__no_pips_for_no_gaps(point_num, expected_isight):
    """Add 1 pip for each empty space on points 4, 5, or 6 (only if the other player has
    a checker on his corresponding point);"""
    board = Board()
    board.points[point_num].num_checkers = 1
    board.points[point_num].color = Team.X
    board.points[25 - point_num].num_checkers = 1
    board.points[25 - point_num].color = Team.O
    assert iSight(board) == expected_isight


@pytest.mark.parametrize(
    "point_num, expected_isight",
    [
        (7, 11),  # 4 pips + 1 crossover
        (13, 18),  # 13 pips + 2 crossovers
        (24, 27),  # 24 pips + 3 crossovers
    ],
)
def test_iSight__crossovers(point_num, expected_isight):
    """Add 1 pip for each additional crossover compared to the opponent."""
    board = Board()
    board.points[point_num].num_checkers = 1
    board.points[point_num].color = Team.X
    assert iSight(board) == expected_isight


@pytest.mark.parametrize(
    "point_num_X, point_num_O, expected_isight",
    [
        (7, 18, 7),  # 7 pips + 1 crossover - 1 crossover
        (13, 14, 14),  # 13 pips + 2 crossover - 1 crossover
        (24, 23, 27),  # 24 pips + 3 crossover - 0 crossovers
    ],
)
def test_iSight__crossover_difference(point_num_X, point_num_O, expected_isight):
    """Add 1 pip for each additional crossover compared to the opponent."""
    board = Board()
    board.points[point_num_X].num_checkers = 1
    board.points[point_num_X].color = Team.X

    board.points[point_num_O].num_checkers = 1
    board.points[point_num_O].color = Team.O

    assert iSight(board) == expected_isight
