from dataclasses import dataclass
from enum import StrEnum
from typing import NamedTuple, Optional


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

    def display(self) -> None:
        """Displays the board in the command line."""
        for point in self.points:
            if point.num_checkers:
                print(f"{point.number: 03d}: {point.color * point.num_checkers}")
            else:
                print(f"{point.number: 03d}:")

    def get_pipcount(self) -> PipCount:
        """Calculates and returns the pip count for each player."""
        X_count = sum(point.number * point.num_checkers for point in self.points if point.color == Team.X)
        O_count = sum((25 - point.number) * point.num_checkers for point in self.points if point.color == Team.O)
        return PipCount(X=X_count, O=O_count)
