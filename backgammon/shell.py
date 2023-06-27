from collections import defaultdict
from pathlib import Path
from time import sleep

from backgammon import colors
from backgammon.board import Board, Team

board_left_file = Path(__file__).parent / "board_left.txt"
with open(board_left_file, 'r') as f:
    board_left = ''.join(f.readlines())

board_right_file = Path(__file__).parent / "board_right.txt"
with open(board_right_file, 'r') as f:
    board_right = ''.join(f.readlines())


def clear_lines(n: int = 1) -> None:
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def welcome():
    print('Welcome to the Backgammon Trainer!')


def read_int(prompt: str) -> int:
    while True:
        try:
            output = int(input(prompt).strip().split()[0])
            return output
        except ValueError:
            print('Please provide a valid integer.')


def read_choice(prompt: str, choices: list[int]) -> int:
    while (choice := read_int(prompt)) not in choices:
        print('Please select a valid number.')
    return choice


def select_game() -> int:
    prompt = 'Please select a game\n'
    prompt += '1. Point number trainer\n'
    return read_choice(prompt, [1])


def bear_off_question() -> bool:
    prompt = 'What direction would you like to bear off?\n'
    prompt += '1. Left\n2. Right\n'
    direction = read_choice(prompt)
    return True if direction == 1 else False


def print_board(board: Board, show_points: bool = True):
    labels = defaultdict(lambda: '  ')
    labels.update({'BAR': colors.y("BAR"), 'OFF': colors.y("OFF"), 'even': colors.y("░░"), 'odd': '░░'})

    if show_points:
        labels.update({f'p{i}': f"{i:02}" for i in range(1, 25)})

    X = [colors.r(" X"), colors.r("XX"), colors.r("3X")]
    O = [colors.g(" O"), colors.g("OO"), colors.g("3O")]

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
    for point, checkers in [[board.points[0], O], [board.points[25], X]]:
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
        print('.' * i, end='\r')
        sleep(1)
    print('\n ')


if __name__ == '__main__':
    while True:
        out = read_int('give me an int')
        print(out)
        print(type(out))
