import random
from dataclasses import dataclass
from enum import StrEnum
from typing import NamedTuple, Optional


class InvalidMove(Exception):
    """Raised when user tries to make an invalid checker play"""


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
    """A backgammon board, comprised of 24 points and the bar point for X (25) and
    the bar point for O (0). The X team represents the user, and the O team represents
    the opponent."""

    def __init__(self, bear_off_left: bool = True):
        self.points = [Point(i) for i in range(26)]
        self.bear_off_left = bear_off_left

    def reset(self):
        for point in self.points:
            point.num_checkers = 0
            point.color = None

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

    def random_point(self):
        self.reset()
        point_num = random.randint(1, 24)
        self.points[point_num].num_checkers = 1
        self.points[point_num].color = Team.X

    def random_board(self, bar: bool = False, max_checkers: int = 5):
        self.reset()
        touched_points = []

        for color in [Team.X, Team.O]:
            remaining_checkers = 15
            while remaining_checkers > 0:
                if bar:
                    point_num = random.randint(0, 26)
                else:
                    point_num = random.randint(1, 25)
                if point_num in touched_points:
                    continue

                touched_points.append(point_num)
                num_checkers = random.randint(1, max_checkers)
                if num_checkers > remaining_checkers:
                    num_checkers = remaining_checkers
                remaining_checkers = remaining_checkers - num_checkers

                self.points[point_num].num_checkers = num_checkers
                self.points[point_num].color = color

    @property
    def points_with_checkers(self) -> list[Point]:
        return [point for point in self.points if point.num_checkers > 0]

    @property
    def pipcount(self) -> PipCount:
        """Calculates and returns the pip count for each player."""
        X_count = sum(point.number * point.num_checkers for point in self.points if point.color == Team.X)
        O_count = sum((25 - point.number) * point.num_checkers for point in self.points if point.color == Team.O)
        return PipCount(X=X_count, O=O_count)

    def move_checkers(self, from_pt: int, to_pt: int, num_checkers: int = 1):
        from_pt = self.points[from_pt]
        to_pt = self.points[to_pt]
        if num_checkers > from_pt.num_checkers:
            raise InvalidMove(f"Not enough checkers on point ({from_pt.num_checkers}) to move {num_checkers} checkers")

        if from_pt.color != to_pt.color and to_pt.color is not None:
            if to_pt.num_checkers > 1:
                raise InvalidMove(
                    f"Opponent is in control of the {to_pt.number}-point with {to_pt.num_checkers} checkers"
                    )
            else:
                self.hit_checker(to_pt.number)

        for _ in range(num_checkers):
            to_pt.num_checkers += 1
            from_pt.num_checkers -= 1
        to_pt.color = from_pt.color

        if from_pt.num_checkers == 0:
            from_pt.color = None


    def hit_checker(self, pt: int) -> None:
        point = self.points[pt]
        if point.num_checkers > 1:
            raise InvalidMove(f"Too many checkers to hit ({point.num_checkers})")
        if point.num_checkers < 1:
            raise InvalidMove(f"No checkers to hit on {point.number} point.")

        if point.color == Team.X:
            self.points[25].num_checkers += 1
            self.points[25].color = Team.X
        elif point.color == Team.O:
            self.points[0].num_checkers += 1
            self.points[0].color = Team.O
        point.num_checkers = 0
