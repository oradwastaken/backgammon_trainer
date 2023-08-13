from bgtrainer.database import con
from datetime import datetime

c = con.cursor()


def add_score(score: float, game: str) -> None:
    with con:
        c.execute(
            """INSERT INTO scores VALUES (:time, :game, :score)""",
            {"time": datetime.now(), "game": game, "score": score},
        )


def high_score(game) -> float:
    highest_score = con.execute(
        """SELECT score FROM scores WHERE game = ? ORDER BY score DESC""", (game,)
    ).fetchone()
    return highest_score[0]


con.close()
