from collections import defaultdict
from time import sleep

from backgammon import colors
from backgammon.board import Board, Team

board_left = '\n'
board_left += '║ {OFF} ║ {p24} ║ {p23} ║ {p22} ║ {p21} ║ {p20} ║ {p19} ║ {BAR} ║ {p18} ║ {p17} ║ {p16} ║ {p15} ║ {p14} ║ {p13} ║\n'
board_left += '╠═════╬════╩════╩════╩════╩════╩════╬═════╬════╩════╩════╩════╩════╩════╣\n'
board_left += '║     ║ {even}   {odd}   {even}   {odd}   {even}   {odd} ║     ║ {even}   {odd}   {even}   {odd}   {even}   {odd} ║\n'
board_left += '║     ║ {24_1}   {23_1}   {22_1}   {21_1}   {20_1}   {19_1} ║     ║ {18_1}   {17_1}   {16_1}   {15_1}   {14_1}   {13_1} ║\n'
board_left += '║     ║ {24_2}   {23_2}   {22_2}   {21_2}   {20_2}   {19_2} ║ {0_3}  ║ {18_2}   {17_2}   {16_2}   {15_2}   {14_2}   {13_2} ║\n'
board_left += '║     ║ {24_3}   {23_3}   {22_3}   {21_3}   {20_3}   {19_3} ║ {0_2}  ║ {18_3}   {17_3}   {16_3}   {15_3}   {14_3}   {13_3} ║\n'
board_left += '║     ║ {24_4}   {23_4}   {22_4}   {21_4}   {20_4}   {19_4} ║ {0_1}  ║ {18_4}   {17_4}   {16_4}   {15_4}   {14_4}   {13_4} ║\n'
board_left += '║     ║ {24_5}   {23_5}   {22_5}   {21_5}   {20_5}   {19_5} ║     ║ {18_5}   {17_5}   {16_5}   {15_5}   {14_5}   {13_5} ║\n'
board_left += '║     ║                             ║ {BAR} ║                             ║\n'
board_left += '║     ║ {1_5}   {2_5}   {3_5}   {4_5}   {5_5}   {6_5} ║     ║ {7_5}   {8_5}   {9_5}   {10_5}   {11_5}   {12_5} ║    \n'
board_left += '║     ║ {1_4}   {2_4}   {3_4}   {4_4}   {5_4}   {6_4} ║ {25_1}  ║ {7_4}   {8_4}   {9_4}   {10_4}   {11_4}   {12_4} ║    \n'
board_left += '║     ║ {1_3}   {2_3}   {3_3}   {4_3}   {5_3}   {6_3} ║ {25_2}  ║ {7_3}   {8_3}   {9_3}   {10_3}   {11_3}   {12_3} ║    \n'
board_left += '║     ║ {1_2}   {2_2}   {3_2}   {4_2}   {5_2}   {6_2} ║ {25_3}  ║ {7_2}   {8_2}   {9_2}   {10_2}   {11_2}   {12_2} ║    \n'
board_left += '║     ║ {1_1}   {2_1}   {3_1}   {4_1}   {5_1}   {6_1} ║     ║ {7_1}   {8_1}   {9_1}   {10_1}   {11_1}   {12_1} ║    \n'
board_left += '║     ║ {odd}   {even}   {odd}   {even}   {odd}   {even} ║     ║ {odd}   {even}   {odd}   {even}   {odd}   {even} ║\n'
board_left += '╠═════╬════╦════╦════╦════╦════╦════╬═════╬════╦════╦════╦════╦════╦════╣\n'
board_left += '║ {OFF} ║ {p1} ║ {p2} ║ {p3} ║ {p4} ║ {p5} ║ {p6} ║ {BAR} ║ {p7} ║ {p8} ║ {p9} ║ {p10} ║ {p11} ║ {p12} ║\n'

board_right = '\n'
board_right += '║ {p13} ║ {p14} ║ {p15} ║ {p16} ║ {p17} ║ {p18} ║ {BAR} ║ {p19} ║ {p20} ║ {p21} ║ {p22} ║ {p23} ║ {p24} ║ {OFF} ║\n'
board_right += '╠════╩════╩════╩════╩════╩════╬═════╬════╩════╩════╩════╩════╩════╬═════╣\n'
board_right += '║ {odd}   {even}   {odd}   {even}   {odd}   {even} ║     ║ {odd}   {even}   {odd}   {even}   {odd}   {even} ║     ║\n'
board_right += '║ {13_1}   {14_1}   {15_1}   {16_1}   {17_1}   {18_1} ║     ║ {19_1}   {20_1}   {21_1}   {22_1}   {23_1}   {24_1} ║     ║\n'
board_right += '║ {13_2}   {14_2}   {15_2}   {16_2}   {17_2}   {18_2} ║ {0_3}  ║ {19_2}   {20_2}   {21_2}   {22_2}   {23_2}   {24_2} ║     ║\n'
board_right += '║ {13_3}   {14_3}   {15_3}   {16_3}   {17_3}   {18_3} ║ {0_2}  ║ {19_3}   {20_3}   {21_3}   {22_3}   {23_3}   {24_3} ║     ║\n'
board_right += '║ {13_4}   {14_4}   {15_4}   {16_4}   {17_4}   {18_4} ║ {0_1}  ║ {19_4}   {20_4}   {21_4}   {22_4}   {23_4}   {24_4} ║     ║\n'
board_right += '║ {13_5}   {14_5}   {15_5}   {16_5}   {17_5}   {18_5} ║     ║ {19_5}   {20_5}   {21_5}   {22_5}   {23_5}   {24_5} ║     ║\n'
board_right += '║                             ║ {BAR} ║                             ║     ║\n'
board_right += '║ {12_5}   {11_5}   {10_5}   {9_5}   {8_5}   {7_5} ║     ║ {6_5}   {5_5}   {4_5}   {3_5}   {2_5}   {1_5} ║     ║\n'
board_right += '║ {12_4}   {11_4}   {10_4}   {9_4}   {8_4}   {7_4} ║ {25_1}  ║ {6_4}   {5_4}   {4_4}   {3_4}   {2_4}   {1_4} ║     ║\n'
board_right += '║ {12_3}   {11_3}   {10_3}   {9_3}   {8_3}   {7_3} ║ {25_2}  ║ {6_3}   {5_3}   {4_3}   {3_3}   {2_3}   {1_3} ║     ║\n'
board_right += '║ {12_2}   {11_2}   {10_2}   {9_2}   {8_2}   {7_2} ║ {25_3}  ║ {6_2}   {5_2}   {4_2}   {3_2}   {2_2}   {1_2} ║     ║\n'
board_right += '║ {12_1}   {11_1}   {10_1}   {9_1}   {8_1}   {7_1} ║     ║ {6_1}   {5_1}   {4_1}   {3_1}   {2_1}   {1_1} ║     ║\n'
board_right += '║ {even}   {odd}   {even}   {odd}   {even}   {odd} ║     ║ {even}   {odd}   {even}   {odd}   {even}   {odd} ║     ║\n'
board_right += '╠════╦════╦════╦════╦════╦════╬═════╬════╦════╦════╦════╦════╦════╬═════╣\n'
board_right += '║ {p12} ║ {p11} ║ {p10} ║ {p9} ║ {p8} ║ {p7} ║ {BAR} ║ {p6} ║ {p5} ║ {p4} ║ {p3} ║ {p2} ║ {p1} ║ {OFF} ║\n'


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
