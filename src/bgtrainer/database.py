import sqlite3
from pathlib import Path

con = sqlite3.connect(Path(__file__).parent / "data" / "data.db")

try:
    with con:
        con.execute(
            """CREATE TABLE scores(
                            time TEXT,
                            game TEXT,
                            score REAL
                            )"""
        )
except sqlite3.OperationalError as err:
    if str(err) != "table scores already exists":
        raise

try:
    with con:
        con.execute(
            """CREATE TABLE configs(
                            key TEXT,
                            value TEXT
                            )"""
        )
except sqlite3.OperationalError as err:
    if str(err) != "table configs already exists":
        raise


def cleanup():
    con.close()
