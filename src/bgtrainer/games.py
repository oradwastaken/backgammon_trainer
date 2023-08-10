import csv
import random
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any, Optional
from abc import ABC, abstractmethod

from bgtrainer.board import Board, Move
from bgtrainer.shell import (
    print_board,
    read_int,
    read_move,
    read_pipcount,
    read_yesno,
    wait,
    )


def by_pairs(iterable):
    args = [iter(iterable)] * 2
    return tuple(zip(*args, strict=True))


opening_moves_file = Path(__file__).parent / "data" / "opening_moves.csv"
opening_moves = defaultdict(list)
with opening_moves_file.open("r") as file:
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
    """An object that keeps track of the quiz elements: the score, times, and high scores"""
    num_wins: int = 0
    total_time: float = 0
    total_rounds: int = 10
    round_num: int = 0
    start_time: float = 0
    correct_answers: Optional[list[Any]] = None

    def start_clock(self):
        self.start_time = perf_counter()

    def stop_clock(self):
        self.total_time = self.total_time + (perf_counter() - self.start_time)

    def setup_game(self):
        self.num_wins = 0
        self.total_time = 0
        self.round_num = 0

    def you_win(self):
        self.num_wins += 1
        print("Right! 😎")

    def you_lose(self, ):
        print("Oh no! 😢")
        if self.correct_answers is not None:
            correct_answers_str = " ".join([str(answer) for answer in self.correct_answers])
            print(f"The correct answer was {correct_answers_str}")

    def show_score(self):
        print(f"\nScore: {self.num_wins}/{self.round_num}")

    def show_final_score(self):
        print(f"Final score: {self.num_wins}/{self.total_rounds}!")
        print(f"Total time: {self.total_time:.1f} s")
        print(f"Average time: {self.total_time / self.total_rounds:.1f} s/round")


class Game(ABC):
    board: Board
    quiz: Quiz

    @abstractmethod
    def play(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def setup_board(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def play_round(self) -> bool:
        raise NotImplementedError


@dataclass
class PointNumber(Game):
    board: Board = field(default_factory=Board)
    quiz: Quiz = field(default_factory=Quiz)

    def play(self):
        self.quiz.play()

    def setup_board(self):
        self.board.reset()
        self.board.random_point()
        correct_answer = self.board.points_with_checkers[0].number
        return [correct_answer]

    def play_round(self) -> bool:
        print_board(self.board, show_points=False)
        prompt = "What point is the checker on?\n  "
        start_time = perf_counter()
        guess = read_int(prompt)
        self.quiz.total_time += perf_counter() - start_time
        return guess in


@dataclass
class OpeningMoves(Game):
    board: Board = field(default_factory=Board)
    quiz: Quiz = field(default_factory=Quiz)

    def play(self):
        self.quiz.setup_game()
        for self.quiz.round_num in range(1, self.quiz.total_rounds + 1):
            self.play_round()

        self.quiz.show_final_score()

        play_again = read_yesno("\nWould you like to play again? (Y/N)\n")
        if play_again:
            self.play()

    def setup_board(self):
        self.board.setup()
        keys = list(opening_moves)
        dice = random.choice(keys)
        self.quiz.correct_answers = opening_moves[dice]

    def play_round(self) -> bool:
        """Returns true if you win the round"""
        self.setup_board()
        wait(3)
        print_board(self.board, show_points=True)
        prompt = f"You rolled a {dice}\nWhat is your move?\n"
        prompt += "Please provide it in the form: (24/23, 23/22)\n"
        self.quiz.start_clock()
        guess_moves = read_move(prompt)
        self.quiz.stop_clock()
        print(f"Your move: {' '.join([str(move) for move in guess_moves])}")
        win = all(move in self.quiz.correct_answers for move in guess_moves)

        if win:
            self.quiz.you_win()
        else:
            self.quiz.you_lose()
        self.quiz.show_score()
        return win


@dataclass
class PipCountGame(Game):
    board: Board = field(default_factory=Board)
    quiz: Quiz = field(default_factory=Quiz)
    show_points: bool = False

    def play(self):
        response = read_yesno("\nWould you like to see the point numbers? (Y/N)\n")
        self.show_points = response
        self.quiz.play()

    def setup_board(self):
        self.board.random_board()
        return [self.board.pipcount]

    def play_round(self, correct_answers) -> bool:
        print_board(self.board, show_points=self.show_points)
        prompt = "What are the two pip counts?\n"
        prompt += "Please provide it in the form: X=167, O=167\n"
        start_time = perf_counter()
        guess = read_pipcount(prompt)
        self.quiz.total_time += perf_counter() - start_time
        return guess in [correct_answers]


games = {1: PointNumber, 2: OpeningMoves, 3: PipCountGame}

if __name__ == "__main__":
    point_number_game = PointNumber(Board())
    point_number_game.play()
