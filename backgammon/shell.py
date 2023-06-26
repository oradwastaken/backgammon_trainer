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


def read_int(prompt: str) -> int:
    output = None
    while output is None:
        try:
            output = int(input(prompt).strip().split()[0])
            return output
        except ValueError:
            print('Please provide a valid integer.')


def print_board(board: Board, show_points: bool = True):
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
    XXX = colors.r("3X")
    OOO = colors.g("3O")

    for point in board.points_with_checkers:
        checker = X if point.color == Team.X else O
        for i in range(point.num_checkers):
            labels.update({f"{point.number}_{i % 5 + 1}": checker})

        # If there are 6 or more checkers, start adding multiple in each row:
        checker = XX if point.color == Team.X else OO
        for i in range(5, point.num_checkers):
            labels.update({f"{point.number}_{i % 5 + 1}": checker})

        checker = XXX if point.color == Team.X else OOO
        for i in range(10, point.num_checkers):
            labels.update({f"{point.number}_{i % 5 + 1}": checker})

    # Checkers on the bar are special cases:
    point = board.points[0]
    if point.num_checkers > 0:
        for i in range(point.num_checkers):
            labels.update({f"{point.number}_{i % 3 + 1}": O})
        for i in range(3, point.num_checkers):
            labels.update({f"{point.number}_{i % 3 + 1}": OO})
        for i in range(6, point.num_checkers):
            labels.update({f"{point.number}_{i % 3 + 1}": OOO})

    point = board.points[25]
    if point.num_checkers > 0:
        for i in range(point.num_checkers):
            labels.update({f"{point.number}_{i % 3 + 1}": X})
        for i in range(3, point.num_checkers):
            labels.update({f"{point.number}_{i % 3 + 1}": XX})
        for i in range(6, point.num_checkers):
            labels.update({f"{point.number}_{i % 3 + 1}": XXX})

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
