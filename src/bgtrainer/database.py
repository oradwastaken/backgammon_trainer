import sqlite3
from datetime import datetime
from pathlib import Path

con = sqlite3.connect(Path(__file__).parent / "data" / "data.db")

with con:
    con.execute(
        """CREATE TABLE IF NOT EXISTS scores(
                            time TEXT,
                            game TEXT,
                            score REAL
                            )"""
    )

with con:
    con.execute(
        """CREATE TABLE IF NOT EXISTS configs(
                            key TEXT,
                            value TEXT
                            )"""
    )


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


def reset_scores() -> None:
    with con:
        con.execute("""DROP TABLE scores""")
