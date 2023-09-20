import json
import random
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple, Optional


class InvalidMove(Exception):
    """Raised when user tries to make an invalid checker play."""


class Move(NamedTuple):
    from_pt: int
    to_pt: int
    num_checkers: int = 1

    def __str__(self):
        if self.num_checkers > 1:
            return f"{self.from_pt}/{self.to_pt}({self.num_checkers})"
        return f"{self.from_pt}/{self.to_pt}"


class PipCount(NamedTuple):
    X: int
    O: int  # noqa: E741


class CrossoverCount(NamedTuple):
    X: int
    O: int  # noqa: E741


class Team(StrEnum):
    X = "X"
    O = "O"  # noqa: E741


class Point:
    """Represents a point on the board."""

    __slots__ = ("_number", "num_checkers", "_color")

    def __init__(self, number: int, num_checkers: int = 0, color: Optional[Team] = None):
        self._number = number
        self.num_checkers = num_checkers
        self._color = color

    @property
    def number(self):
        """Once a point is set and created, it shouldn't be changeable."""
        return self._number

    @property
    def color(self) -> Optional[Team]:
        if self.num_checkers == 0:
            return None
        return self._color

    @color.setter
    def color(self, color: Optional[Team]) -> None:
        self._color = color


class Board:
    """A backgammon board, comprised of 24 points and the bar point for X (25) and the
    bar point for O (0).

    The X team represents the user, and the O team represents the opponent.
    """

    __slots__ = ("points", "bear_off_left")

    def __init__(self, points: Optional[list[Point]] = None, bear_off_left: bool = True):
        self.points: list[Point] = [Point(i) for i in range(26)] if points is None else points
        self.bear_off_left = bear_off_left

    def reset(self) -> None:
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

    def random_point(self) -> None:
        self.reset()
        point_num = random.randint(1, 24)
        self.points[point_num].num_checkers = 1
        self.points[point_num].color = Team.X

    @property
    def points_with_checkers(self) -> list[Point]:
        return [point for point in self.points if point.num_checkers > 0]

    @property
    def num_checkers(self) -> int:
        return sum(point.num_checkers for point in self.points_with_checkers)

    @property
    def pipcount(self) -> PipCount:
        """Calculates and returns the pip count for each player."""
        X_count = sum(
            point.number * point.num_checkers for point in self.points if point.color == Team.X
        )
        O_count = sum(
            (25 - point.number) * point.num_checkers
            for point in self.points
            if point.color == Team.O
        )
        return PipCount(X=X_count, O=O_count)

    @property
    def crossovers(self) -> CrossoverCount:
        """Calculates and returns the number of crossovers for each player."""
        num_crossovers_X = 0
        num_crossovers_O = 0

        for point in self.points_with_checkers:
            if point.color == Team.X:
                if point.number >= 19:
                    num_crossovers_X += 3 * point.num_checkers
                elif 19 > point.number >= 13:
                    num_crossovers_X += 2 * point.num_checkers
                elif 13 > point.number >= 7:
                    num_crossovers_X += 1 * point.num_checkers

            if point.color == Team.O:
                if point.number <= 6:
                    num_crossovers_O += 3 * point.num_checkers
                elif 6 < point.number <= 12:
                    num_crossovers_O += 2 * point.num_checkers
                elif 12 < point.number <= 18:
                    num_crossovers_O += 1 * point.num_checkers

        return CrossoverCount(X=num_crossovers_X, O=num_crossovers_O)

    def move_checkers(self, from_pt_num: int, to_pt_num: int, num_checkers: int = 1) -> None:
        from_pt = self.points[from_pt_num]
        to_pt = self.points[to_pt_num]
        if num_checkers > from_pt.num_checkers:
            raise InvalidMove(
                f"Not enough checkers on point ({from_pt.num_checkers}) "
                f"to move {num_checkers} checkers"
            )

        if from_pt.color != to_pt.color and to_pt.color is not None:
            self.hit_checker(to_pt.number)

        to_pt.num_checkers += num_checkers
        from_pt.num_checkers -= num_checkers
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

    def asdict(self) -> dict:
        out_dict = {
            "bear_off_left": self.bear_off_left,
            "points": [[point.number, point.num_checkers, point.color] for point in self.points],
        }
        return out_dict

    @classmethod
    def load(cls, filename: str | Path):
        with open(filename, "r") as f:
            in_dict = json.load(f)

        return cls(
            bear_off_left=in_dict["bear_off_left"],
            points=[Point(*point) for point in in_dict["points"]],
        )

    def save(self, filename: str | Path):
        with open(filename, "w") as f:
            json.dump(self.asdict(), f)


def random_board(board: Board, bar: bool = False, both_players: bool = False) -> Board:
    board.reset()
    touched_points = []

    if both_players:
        teams = [Team.X, Team.O]
    else:
        teams = [Team.X]

    for color in teams:
        remaining_checkers = 15
        while remaining_checkers > 0:
            if bar:
                point_num = random.randint(0, 25)
            else:
                point_num = random.randint(1, 24)
            if point_num in touched_points:
                continue
            touched_points.append(point_num)

            num_checkers = random.choice([1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6])
            if num_checkers > remaining_checkers:
                num_checkers = remaining_checkers
            remaining_checkers = remaining_checkers - num_checkers

            board.points[point_num].num_checkers = num_checkers
            board.points[point_num].color = color

    return board


def random_bear_off_position(board: Board, both_players: bool = False) -> Board:
    board.reset()
    touched_points = []

    if both_players:
        teams = [Team.X, Team.O]
    else:
        teams = [Team.X]

    for color in teams:
        remaining_checkers = random.choice([15, 15, 15, 15, 14, 14, 14, 13, 12])
        while remaining_checkers > 0:
            if color == Team.X:
                point_num = random.randint(1, 6)
            elif color == Team.O:
                point_num = random.randint(19, 24)
            if point_num in touched_points:
                continue
            touched_points.append(point_num)

            num_checkers = random.choice([1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6])
            if num_checkers > remaining_checkers:
                num_checkers = remaining_checkers

            board.points[point_num].num_checkers = num_checkers
            board.points[point_num].color = color
            remaining_checkers = remaining_checkers - num_checkers

    return board


def iSight(board: Board) -> int:
    count = board.pipcount.X

    num_X_checkers = sum(
        point.num_checkers for point in board.points_with_checkers if point.color == Team.X
    )
    num_O_checkers = sum(
        point.num_checkers for point in board.points_with_checkers if point.color == Team.O
    )
    count += num_X_checkers - num_O_checkers

    count += 2 * max(board.points[1].num_checkers - 2, 0)

    count += 1 * max(board.points[2].num_checkers - 2, 0)

    count += 1 * max(board.points[3].num_checkers - 3, 0)

    if board.points[4].num_checkers == 0 and board.points[21].num_checkers > 0:
        count += 1

    if board.points[5].num_checkers == 0 and board.points[20].num_checkers > 0:
        count += 1

    if board.points[6].num_checkers == 0 and board.points[19].num_checkers > 0:
        count += 1

    num_X_crossovers, num_O_crossovers = board.crossovers
    count += num_X_crossovers - num_O_crossovers
    return count
