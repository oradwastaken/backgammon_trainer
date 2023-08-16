from dataclasses import dataclass

import bgtrainer.shell as sh
from bgtrainer.database import add_score, high_score, reset_scores


@dataclass
class Score:
    name: str
    score: float = 0

    def high_score(self):
        return high_score(self.name)

    def save_score(self):
        add_score(self.score, self.name)

    @staticmethod
    def reset_scores():
        response = sh.read_yesno("\nAre you sure you want to do that? (Y/N)\n")
        if response:
            reset_scores()
