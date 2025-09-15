import random
from dataclasses import dataclass
from typing import List, Tuple, Optional


Board = List[int]


@dataclass
class EvalResult:
    board: Board
    h: int


class ObjectiveCounter:
    """Tracks how many times H() is evaluated."""

    def __init__(self):
        self.count = 0

    def increment(self, n: int = 1) -> None:
        self.count += n


def random_board(n: int, rng: random.Random) -> Board:
    """Generate a random N-Queens board: one queen per column in a random row."""
    return [rng.randrange(n) for _ in range(n)]


def h_attacking_pairs(board: Board, counter: Optional[ObjectiveCounter] = None) -> int:
    """Compute H(board): number of attacking pairs of queens.

    Representation: board[c] = row index of the queen in column c.
    """
    n = len(board)
    # O(N^2) pairwise check (sufficient for these sizes)
    attacks = 0
    for i in range(n):
        ri = board[i]
        for j in range(i + 1, n):
            rj = board[j]
            if ri == rj or abs(i - j) == abs(ri - rj):
                attacks += 1
    if counter is not None:
        # Counting this as one H evaluation
        counter.increment()
    return attacks


def generate_neighbors(board: Board) -> List[Tuple[int, int]]:
    """Generate all neighbor moves as (column, new_row) pairs.

    A neighbor is obtained by moving the queen in a single column to a different row.
    """
    n = len(board)
    moves: List[Tuple[int, int]] = []
    for c in range(n):
        current_row = board[c]
        for r in range(n):
            if r != current_row:
                moves.append((c, r))
    return moves


def apply_move(board: Board, move: Tuple[int, int]) -> Board:
    """Return a new board after applying (column, new_row) move."""
    c, r = move
    new_board = list(board)
    new_board[c] = r
    return new_board


def is_solution(board: Board, counter: Optional[ObjectiveCounter] = None) -> bool:
    return h_attacking_pairs(board, counter) == 0

