from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum
from typing import NamedTuple, Optional

from backgammon import colors


class PipCount(NamedTuple):
    X: int
    O: int


class Team(StrEnum):
    X = 'X'
    O = 'O'


@dataclass(slots=True)
class Point:
    """Represents a point on the board."""
    number: int
    num_checkers: int = 0
    color: Optional[Team] = None


class Board:
    """A backgammon board, comprised of 24 points and the bar point (0).
    The X team represents the user, and the O team represents the opponent."""

    def __init__(self):
        self.points = [Point(i) for i in range(25)]

    def setup(self) -> None:
        """Sets up the standard initial backgammon board."""
        self.points[24].num_checkers = 2
        self.points[24].color = Team.X

        self.points[13].num_checkers = 5
        self.points[13].color = Team.X

        self.points[8].num_checkers = 3
        self.points[8].color = Team.X

        self.points[6].num_checkers = 5
        self.points[6].color = Team.X

        self.points[1].num_checkers = 2
        self.points[1].color = Team.O

        self.points[12].num_checkers = 5
        self.points[12].color = Team.O

        self.points[17].num_checkers = 3
        self.points[17].color = Team.O

        self.points[19].num_checkers = 5
        self.points[19].color = Team.O

    @property
    def points_with_checkers(self) -> list[Point]:
        return [point for point in self.points if point.num_checkers > 0]

    def get_pipcount(self) -> PipCount:
        """Calculates and returns the pip count for each player."""
        X_count = sum(point.number * point.num_checkers for point in self.points if point.color == Team.X)
        O_count = sum((25 - point.number) * point.num_checkers for point in self.points if point.color == Team.O)
        return PipCount(X=X_count, O=O_count)


def print_board(board: Board, show_points=True):
    labels = defaultdict(lambda: '  ')
    labels.update(
            {
                    'BAR': colors.y("BAR"),
                    'OFF': colors.y("OFF"),
                    'even': colors.y("░░"),
                    'odd': '░░',
                    }
            )

    if show_points:
        labels.update({f'p{i}': f"{i:02}" for i in range(1, 25)})

    X = colors.r(" X")
    O = colors.g(" O")
    XX = colors.r("XX")
    OO = colors.g("OO")

    for point in board.points_with_checkers:
        checker = X if point.color == Team.X else O

        for i in range(point.num_checkers):
            labels.update({f"{point.number}_{i + 1}": checker})

        if point.color == Team.X:
            checker = XX
        else:
            checker = OO

        for i in range(5, point.num_checkers):
            labels.update({f"{point.number}_{i % 5 + 1}": checker})

    board = '\n'
    board += '║ {p13} ║ {p14} ║ {p15} ║ {p16} ║ {p17} ║ {p18} ║ {BAR} ║ {p19} ║ {p20} ║ {p21} ║ {p22} ║ {p23} ║ {p24} ║ {OFF} ║\n'
    board += '╠════╩════╩════╩════╩════╩════╬═════╬════╩════╩════╩════╩════╩════╬═════╣\n'
    board += '║ {odd}   {even}   {odd}   {even}   {odd}   {even} ║     ║ {odd}   {even}   {odd}   {even}   {odd}   {even} ║     ║\n'
    board += '║ {13_1}   {14_1}   {15_1}   {16_1}   {17_1}   {18_1} ║     ║ {19_1}   {20_1}   {21_1}   {22_1}   {23_1}   {24_1} ║     ║\n'
    board += '║ {13_2}   {14_2}   {15_2}   {16_2}   {17_2}   {18_2} ║     ║ {19_2}   {20_2}   {21_2}   {22_2}   {23_2}   {24_2} ║     ║\n'
    board += '║ {13_3}   {14_3}   {15_3}   {16_3}   {17_3}   {18_3} ║     ║ {19_3}   {20_3}   {21_3}   {22_3}   {23_3}   {24_3} ║     ║\n'
    board += '║ {13_4}   {14_4}   {15_4}   {16_4}   {17_4}   {18_4} ║  {0_1} ║ {19_4}   {20_4}   {21_4}   {22_4}   {23_4}   {24_4} ║     ║\n'
    board += '║ {13_5}   {14_5}   {15_5}   {16_5}   {17_5}   {18_5} ║     ║ {19_5}   {20_5}   {21_5}   {22_5}   {23_5}   {24_5} ║     ║\n'
    board += '║                             ║ {BAR} ║                             ║     ║\n'
    board += '║ {12_5}   {11_5}   {10_5}   {9_5}   {8_5}   {7_5} ║     ║ {6_5}   {5_5}   {4_5}   {3_5}   {2_5}   {1_5} ║     ║\n'
    board += '║ {12_4}   {11_4}   {10_4}   {9_4}   {8_4}   {7_4} ║  {25_1} ║ {6_4}   {5_4}   {4_4}   {3_4}   {2_4}   {1_4} ║     ║\n'
    board += '║ {12_3}   {11_3}   {10_3}   {9_3}   {8_3}   {7_3} ║     ║ {6_3}   {5_3}   {4_3}   {3_3}   {2_3}   {1_3} ║     ║\n'
    board += '║ {12_2}   {11_2}   {10_2}   {9_2}   {8_2}   {7_2} ║     ║ {6_2}   {5_2}   {4_2}   {3_2}   {2_2}   {1_2} ║     ║\n'
    board += '║ {12_1}   {11_1}   {10_1}   {9_1}   {8_1}   {7_1} ║     ║ {6_1}   {5_1}   {4_1}   {3_1}   {2_1}   {1_1} ║     ║\n'
    board += '║ {even}   {odd}   {even}   {odd}   {even}   {odd} ║     ║ {even}   {odd}   {even}   {odd}   {even}   {odd} ║     ║\n'
    board += '╠════╦════╦════╦════╦════╦════╬═════╬════╦════╦════╦════╦════╦════╬═════╣\n'
    board += '║ {p12} ║ {p11} ║ {p10} ║ {p9} ║ {p8} ║ {p7} ║ {BAR} ║ {p6} ║ {p5} ║ {p4} ║ {p3} ║ {p2} ║ {p1} ║ {OFF} ║\n'

    print(board.format_map(labels))
