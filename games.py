from time import perf_counter, sleep

from backgammon.board import Board, print_board
from backgammon.shell import clear_lines, read_int


def point_number_game():
    board = Board()

    round_num = 0
    total_rounds = read_int('How many rounds would you like to play?\n  ')
    num_wins = 0

    total_time = 0

    while round_num < total_rounds:
        round_num += 1

        board.reset()
        board.random_point()
        print_board(board, show_points=False)
        start_time = perf_counter()
        guess = read_int('What point is the checker on?\n  ')
        if guess == board.get_pipcount().X:
            num_wins += 1
            print('Right! 😎')
        else:
            print('Oh no! 😢')
        total_time += perf_counter() - start_time

        print(f'Score: {num_wins}/{round_num}')
        sleep(2)
        clear_lines(23)

    print(f'Final score: {num_wins}/{round_num}!')
    print(f'Total time: {total_time:.1f} s // {total_time / round_num:.1f} s/round')


if __name__ == '__main__':
    point_number_game()
