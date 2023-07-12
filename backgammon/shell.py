import re
from collections import defaultdict
from pathlib import Path
from time import sleep
from typing import DefaultDict

from backgammon import colors
from backgammon.board import Board, Move, PipCount, Team

logo_file = Path(__file__).parent / "data" / "logo.txt"
with open(logo_file, "r") as f:
    logo = "".join(f.readlines())

board_left_file = Path(__file__).parent / "data" / "board_left.txt"
with open(board_left_file, "r") as f:
    board_left = "".join(f.readlines())

board_right_file = Path(__file__).parent / "data" / "board_right.txt"
with open(board_right_file, "r") as f:
    board_right = "".join(f.readlines())


def clear_lines(n: int = 1) -> None:
    LINE_UP = "\033[1A"
    LINE_CLEAR = "\x1b[2K"
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def welcome():
    print(logo)


def read_int(prompt: str) -> int:
    while True:
        try:
            output = int(input(prompt).strip().split()[0])
            return output
        except (ValueError, IndexError):
            print("Please provide a valid integer.")


def read_choice(prompt: str, choices: list[int]) -> int:
    while (choice := read_int(prompt)) not in choices:
        print("Please select a valid number.")
    return choice


def read_yesno(prompt: str) -> bool:
    while (answer := input(prompt).strip()) not in ["Y", "y", "N", "n"]:
        print("Please provide a valid response (Y/N).")
    return answer.upper() == "Y"


def parse_moves(move_str: str) -> list[Move]:
    """Converts a move of the form (24/23), (24/23, 23/22) or 24/23 to a list of
    Moves."""
    moves = [
        Move(*[int(pt) for pt in move.split(sep="/")]) for move in re.findall(r"\d+/\d+", move_str)
    ]
    return moves


def read_move(prompt: str) -> list[Move]:
    while (moves := parse_moves(input(prompt))) == []:
        print("Please provide a valid checker move of the form: (24/23, 23/22).")
    return moves


def parse_pipcounts(pipcount_str: str) -> PipCount:
    X_pips = re.findall(r"X=\d+", pipcount_str.upper())
    X_pips_num = int(X_pips[0].split(sep="=")[-1])
    O_pips = re.findall(r"O=\d+", pipcount_str.upper())
    O_pips_num = int(O_pips[0].split(sep="=")[-1])
    return PipCount(X=X_pips_num, O=O_pips_num)


def read_pipcount(prompt: str) -> PipCount:
    while True:
        try:
            return parse_pipcounts(input(prompt))
        except (ValueError, IndexError):
            print("Please provide a valid pip count of the form: X=167, O=167")


def select_game() -> int:
    prompt = "Please select a game\n"
    prompt += "1. Point number trainer\n"
    prompt += "2. Opening move trainer\n"
    prompt += "3. Pip counting trainer\n"
    return read_choice(prompt, [1, 2, 3])


def bear_off_question() -> bool:
    prompt = "What direction would you like to bear off?\n"
    prompt += "1. Left\n2. Right\n"
    direction = read_choice(prompt, [1, 2])
    return True if direction == 1 else False


def print_board(board: Board, show_points: bool = True):
    labels: DefaultDict[str, str] = defaultdict(lambda: "  ")
    labels.update(
        {"BAR": colors.y("BAR"), "OFF": colors.y("OFF"), "even": colors.y("░░"), "odd": "░░"}
    )

    if show_points:
        labels.update({f"p{i}": f"{i:02}" for i in range(1, 25)})

    X = [colors.r(" X"), colors.r("XX"), colors.r("3X")]
    O = [colors.g(" O"), colors.g("OO"), colors.g("3O")]  # noqa: E741

    for point in board.points_with_checkers:
        checkers = X if point.color == Team.X else O
        for i in range(point.num_checkers):
            labels.update({f"{point.number}_{i % 5 + 1}": checkers[0]})

        # If there are 6 or more checkers, replace with multiple in each spot:
        for i in range(5, point.num_checkers):
            labels.update({f"{point.number}_{i % 5 + 1}": checkers[1]})
        for i in range(10, point.num_checkers):
            labels.update({f"{point.number}_{i % 5 + 1}": checkers[2]})

    # Checkers on the bar are special cases:
    for point, checkers in zip([board.points[0], board.points[25]], [O, X]):
        if point.num_checkers > 0:
            for i in range(point.num_checkers):
                labels.update({f"{point.number}_{i % 3 + 1}": checkers[0]})
            for i in range(3, point.num_checkers):
                labels.update({f"{point.number}_{i % 3 + 1}": checkers[1]})
            for i in range(6, point.num_checkers):
                labels.update({f"{point.number}_{i % 3 + 1}": checkers[2]})

    if board.bear_off_left:
        print(board_left.format_map(labels))
    else:
        print(board_right.format_map(labels))


def wait(seconds: int):
    for i in range(1, seconds + 1):
        print("." * (seconds + 1 - i) + " " * i, end="\r")
        sleep(1)
    print(" \n ", end="\r")


if __name__ == "__main__":
    while True:
        out = read_int("give me an int")
        print(out)
        print(type(out))
