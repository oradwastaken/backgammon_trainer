from dataclasses import dataclass
from datetime import datetime

import bgtrainer.colors as c
from bgtrainer.database import con


def add_score(score: float, game: str) -> None:
    with con:
        con.execute(
            """INSERT INTO scores VALUES (:time, :game, :score)""",
            {"time": datetime.now(), "game": game, "score": score},
        )


def high_score(game) -> float:
    with con:
        highest_score = con.execute(
            """SELECT score FROM scores WHERE game = ? ORDER BY score DESC""", (game,)
        ).fetchone()
    if highest_score is None:
        return 0
    return highest_score[0]


@dataclass
class Score:
    name: str
    score: float = 0

    @staticmethod
    def congratulate():
        print(f"New High Score{c.r('!')}{c.y('!')}{c.g('!')}{c.b('!')}{c.m('!')}")

    def high_score(self):
        return high_score(self.name)

    def save_score(self):
        add_score(self.score, self.name)
