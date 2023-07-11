import csv
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from backgammon.board import Board, Move
from backgammon.shell import print_board, read_int, read_move, wait


def by_pairs(iterable):
    args = [iter(iterable)] * 2
    return tuple(zip(*args, strict=True))


opening_moves_file = Path(__file__).parent / "data" / "opening_moves.csv"
opening_moves = defaultdict(list)
with open(opening_moves_file, "r") as file:
    csvreader = csv.reader(file)
    next(csvreader, None)  # skip the headers
    for row in csvreader:
        row_ints = [int(item) for item in row if item != ""]
        dice1, dice2, *remainder = row
        dice = (dice1, dice2)
        moves = [Move(a, b) for a, b in by_pairs(remainder)]
        moves.sort()
        opening_moves[dice].append(moves)


@dataclass
class Quiz:
    board: Board
    num_wins: int = 0
    total_time: float = 0
    total_rounds: int = 10
    round_num: int = 0

    def play(self):
        for self.round_num in range(1, self.total_rounds + 1):
            correct_answers = self.setup_board()
            win = self.play_round(correct_answers)
            if win:
                self.you_win()
            else:
                self.you_lose(correct_answers)
            self.show_score()

        self.show_final_score()

    def setup_board(self):
        raise NotImplementedError

    def play_round(self, correct_answers) -> bool:
        raise NotImplementedError

    def you_win(self):
        self.num_wins += 1
        print("Right! 😎")

    def you_lose(self, correct_answers):
        print("Oh no! 😢")
        print(f"The correct answer was {correct_answers}")

    def show_score(self):
        print(f"\nScore: {self.num_wins}/{self.round_num}")
        wait(3)

    def show_final_score(self):
        print(f"Final score: {self.num_wins}/{self.total_rounds}!")
        print(f"Total time: {self.total_time:.1f} s")
        print(f"Average time: {self.total_time / self.total_rounds:.1f} s/round")


@dataclass
class PointNumber(Quiz):
    def setup_board(self):
        self.board.reset()
        self.board.random_point()
        correct_answer = self.board.points_with_checkers[0].number
        return [correct_answer]

    def play_round(self, correct_answers) -> bool:
        print_board(self.board, show_points=False)
        prompt = "What point is the checker on?\n  "
        start_time = perf_counter()
        guess = read_int(prompt)
        self.total_time += perf_counter() - start_time
        return guess in correct_answers


@dataclass
class OpeningMoves(Quiz):
    def setup_board(self):
        self.board.setup()
        keys = list(opening_moves)
        dice = random.choice(keys)
        correct_answers = opening_moves[dice]
        return correct_answers

    def play_round(self, correct_answers) -> bool:
        print_board(self.board, show_points=True)
        prompt = f"You rolled a {dice}\nWhat is your move?\n"
        prompt += "Please provide it in the form (24/23, 23/22)\n"
        start_time = perf_counter()
        guess = read_move(prompt)
        self.total_time += perf_counter() - start_time
        return guess in correct_answers


games = {1: PointNumber, 2: OpeningMoves}

if __name__ == "__main__":
    point_number_game = PointNumber(Board())
    point_number_game.play()
