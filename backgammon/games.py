import csv
import random
from collections import defaultdict
from pathlib import Path
from time import perf_counter

from backgammon.board import Board, Move
from backgammon.shell import print_board, read_int, read_move, wait


def by_pairs(iterable):
    args = [iter(iterable)] * 2
    return tuple(zip(*args, strict=True))


def point_number_game(board: Board):
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
        guess = read_int("What point is the checker on?\n  ")
        total_time += perf_counter() - start_time

        if guess == correct_answer:
            num_wins += 1
            print("Right! 😎")
        else:
            print("Oh no! 😢")
            print(f"The correct answer was {correct_answer}")
        print(f"\nScore: {num_wins}/{round_num}")
        wait(3)

    print(f"Final score: {num_wins}/{total_rounds}!")
    print(f"Total time: {total_time:.1f} s")
    print(f"Average time: {total_time / total_rounds:.1f} s/round")


opening_moves_file = Path(__file__).parent / "data" / "opening_moves.csv"
opening_moves = defaultdict(list)
with open(opening_moves_file, "r") as file:
    csvreader = csv.reader(file)
    next(csvreader, None)  # skip the headers
    for row in csvreader:
        row = (int(item) for item in row if item != "")
        row = (int(item) for item in row)
        dice1, dice2, *remainder = row
        dice = (dice1, dice2)
        moves = [Move(a, b) for a, b in by_pairs(remainder)]
        moves.sort()
        opening_moves[dice].append(moves)


def opening_moves_game(board: Board):
    num_wins = 0
    total_time = 0
    total_rounds = 10

    for round_num in range(1, total_rounds + 1):
        keys = list(opening_moves)
        dice = random.choice(keys)

        board.setup()
        correct_answers = opening_moves[dice]

        print_board(board, show_points=True)
        start_time = perf_counter()
        prompt = f"You rolled a {dice}\nWhat is your move?\n"
        prompt += "Please provide it in the form (24/23, 23/22)\n"
        guess = read_move(prompt)
        total_time += perf_counter() - start_time

        if sorted(guess) in correct_answers:
            num_wins += 1
            print("Right! 😎")
        else:
            print("Oh no! 😢")
            print(f"The correct answer was {correct_answers}")
            breakpoint()
        print(f"\nScore: {num_wins}/{round_num}")
        wait(3)

    print(f"Final score: {num_wins}/{total_rounds}!")
    print(f"Total time: {total_time:.1f} s")
    print(f"Average time: {total_time / total_rounds:.1f} s/round")


games = {1: point_number_game, 2: opening_moves_game}

if __name__ == "__main__":
    point_number_game(Board())
