import random
import time
from dataclasses import dataclass
from typing import List, Callable

try:
    from .nqueens import (
        Board,
        ObjectiveCounter,
        random_board,
        h_attacking_pairs,
    )
except ImportError:  # Allow running as a standalone script
    import os
    import sys
    sys.path.append(os.path.dirname(__file__))
    from nqueens import (  # type: ignore
        Board,
        ObjectiveCounter,
        random_board,
        h_attacking_pairs,
    )


@dataclass
class RSResult:
    board: Board
    h: int
    states_evaluated: int
    time_sec: float
    history_h: List[int]
    seed: int
    n: int


def random_search(
    n: int,
    seed: int,
    max_states_evaluated: int,
    verbose: bool = False,
    print_fn: Callable[[str], None] = print,
) -> RSResult:
    """Pure random sampling until solution or max H evaluations."""
    rng = random.Random(seed)
    counter = ObjectiveCounter()
    start = time.time()

    best_board = random_board(n, rng)
    best_h = h_attacking_pairs(best_board, counter)
    # Registrar el H inicial
    history_h: List[int] = [best_h]
    if verbose:
        print_fn(f"[RND] Start n={n}, seed={seed}, max_states={max_states_evaluated}, init_H={best_h}")

    while counter.count < max_states_evaluated and best_h > 0:
        b = random_board(n, rng)
        h = h_attacking_pairs(b, counter)
        # Registrar cada intento (no solo mejoras)
        history_h.append(h)
        if h < best_h:
            best_board, best_h = b, h
            if verbose:
                print_fn(f"[RND] New best H={best_h}, states={counter.count}")
        # Early exit if solution found
        if best_h == 0:
            break

    elapsed = time.time() - start
    return RSResult(
        board=list(best_board),
        h=best_h,
        states_evaluated=counter.count,
        time_sec=elapsed,
        history_h=history_h,
        seed=seed,
        n=n,
    )


__all__ = ["random_search", "RSResult"]
