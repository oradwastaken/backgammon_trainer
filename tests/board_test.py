import pytest

from bgtrainer.board import Board, Point, Team


def test_Point__default_is_empty():
    point = Point(0)
    assert point.num_checkers == 0
    assert point.color is None


def test_Point__setting_to_0_checkers_removes_color():
    point = Point(0, 3, Team.X)
    point.num_checkers = 0
    assert point.color is None


def test_Point__cant_change_point_number():
    point0 = Point(0)
    with pytest.raises(AttributeError) as err_info:
        point0.number = 1
    assert "object has no setter" in str(err_info.value)
    assert point0.number == 0


def test_Point__change_colors():
    point = Point(0)
    assert point.color is None

    point.num_checkers = 1
    point.color = Team.X
    assert point.color == Team.X

    point.color = Team.O
    assert point.color == Team.O


@pytest.mark.parametrize(
    "point_number, number_crossovers",
    [
        (5, 0),
        (8, 1),
        (13, 2),
        (20, 3),
    ],
)
def test_Board__crossovers_X(point_number, number_crossovers):
    board = Board()
    board.points[point_number].num_checkers = 1
    board.points[point_number].color = Team.X
    assert board.crossovers.X == number_crossovers


@pytest.mark.parametrize(
    "point_number, number_crossovers",
    [
        (5, 3),
        (8, 2),
        (13, 1),
        (20, 0),
    ],
)
def test_Board__crossovers_O(point_number, number_crossovers):
    board = Board()
    board.points[point_number].num_checkers = 1
    board.points[point_number].color = Team.O
    assert board.crossovers.O == number_crossovers
