from time import perf_counter

from backgammon.board import Board
from backgammon.shell import print_board, read_int, wait


def point_number_game(board:Board):


    num_wins = 0
    total_time = 0
    total_rounds = 10
    # while (total_rounds := read_int('How many rounds would you like to play?\n  ')) < 0:
    #     print('Please provide a positive number.')

    for round_num in range(1, total_rounds + 1):
        board.reset()
        board.random_point()
        correct_answer = board.points_with_checkers[0].number

        print_board(board, show_points=False)
        start_time = perf_counter()
        guess = read_int('What point is the checker on?\n  ')
        total_time += perf_counter() - start_time

        if guess == correct_answer:
            num_wins += 1
            print('Right! 😎')
        else:
            print('Oh no! 😢')
            print(f"The correct answer was {correct_answer}")
        print(f'\nScore: {num_wins}/{round_num}')
        wait(3)

    print(f'Final score: {num_wins}/{total_rounds}!')
    print(f'Total time: {total_time:.1f} s')
    print(f'Average time: {total_time / total_rounds:.1f} s/round')


games = {1: point_number_game}

if __name__ == '__main__':
    point_number_game()
