from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

from helpers import get_data


class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    WIN = 1
    LOSE = 2
    DRAW = 3


game = namedtuple("Game", ("own", "opponent"))


@dataclass
class Round:
    own: Move
    opponent: Move

    @staticmethod
    def from_row(line: str):
        opponent_map = {"A": Move.ROCK, "B": Move.PAPER, "C": Move.SCISSORS}
        own_map = {"X": Move.ROCK, "Y": Move.PAPER, "Z": Move.SCISSORS}
        opponent, own = line.strip().split()

        return Round(opponent=opponent_map[opponent], own=own_map[own])

    @staticmethod
    def from_row_part_2(line: str):
        opponent_map = {"A": Move.ROCK, "B": Move.PAPER, "C": Move.SCISSORS}
        outcome_map = {"X": Outcome.LOSE, "Y": Outcome.DRAW, "Z": Outcome.WIN}
        opponent, outcome = line.strip().split()
        opponent_move = opponent_map[opponent]

        return Round(
            opponent=opponent_move,
            own=Round._get_matching_move(opponent_move, outcome_map[outcome]),
        )

    @staticmethod
    def _get_matching_move(opponent_move: Move, outcome: Outcome):
        match [opponent_move, outcome]:
            case [move, Outcome.DRAW]:
                return move

            case [Move.ROCK, Outcome.WIN]:
                return Move.PAPER
            case [Move.ROCK, Outcome.LOSE]:
                return Move.SCISSORS

            case [Move.PAPER, Outcome.WIN]:
                return Move.SCISSORS
            case [Move.PAPER, Outcome.LOSE]:
                return Move.ROCK

            case [Move.SCISSORS, Outcome.WIN]:
                return Move.ROCK
            case [Move.SCISSORS, Outcome.LOSE]:
                return Move.PAPER

    @property
    def winner(self):
        match [self.own, self.opponent]:
            case [own, opponent] if own == opponent:
                return None

            case [Move.ROCK, Move.PAPER]:
                return "opponent"
            case [Move.ROCK, Move.SCISSORS]:
                return "own"

            case [Move.PAPER, Move.ROCK]:
                return "own"
            case [Move.PAPER, Move.SCISSORS]:
                return "opponent"

            case [Move.SCISSORS, Move.ROCK]:
                return "opponent"
            case [Move.SCISSORS, Move.PAPER]:
                return "own"

    @property
    def score(self):
        shape_scores = {Move.ROCK: 1, Move.PAPER: 2, Move.SCISSORS: 3}
        outcome_scores = {"own": 6, None: 3, "opponent": 0}
        return shape_scores[self.own] + outcome_scores[self.winner]


def day_2():
    # data = get_data(2, "example")
    data = get_data(2)
    games = [Round.from_row(line) for line in data]
    print("Part 1: ", sum([game.score for game in games]))

    games_2 = [Round.from_row_part_2(line) for line in data]
    print("Part 2: ", sum([game.score for game in games_2]))


if __name__ == "__main__":
    day_2()
