import math
import random
import time
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

try:
    from .nqueens import (
        Board,
        ObjectiveCounter,
        random_board,
        h_attacking_pairs,
        apply_move,
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
        apply_move,
    )


@dataclass
class SAResult:
    board: Board
    h: int
    states_evaluated: int
    time_sec: float
    history_h: List[int]
    seed: int
    n: int


def _random_neighbor(board: Board, rng: random.Random) -> Board:
    n = len(board)
    c = rng.randrange(n)
    current_row = board[c]
    # choose a different row
    r = rng.randrange(n - 1)
    if r >= current_row:
        r += 1
    return apply_move(board, (c, r))


def _exp_schedule(T0: float, alpha: float, Tmin: float) -> Callable[[int], float]:
    def sched(t: int) -> float:
        return max(T0 * (alpha ** t), Tmin)
    return sched


def _linear_schedule(T0: float, steps: int, Tmin: float) -> Callable[[int], float]:
    # Decrease temperature linearly from T0 to Tmin over `steps` iterations; then clamp
    delta = (T0 - Tmin) / max(1, steps)
    def sched(t: int) -> float:
        return max(T0 - delta * t, Tmin)
    return sched


def simulated_annealing(
    n: int,
    seed: int,
    max_states_evaluated: int,
    schedule: str = "exp",  # "exp" or "linear"
    T0: Optional[float] = None,
    alpha: float = 0.995,
    Tmin: float = 1e-3,
    linear_steps: Optional[int] = None,
    verbose: bool = False,
    print_fn: Callable[[str], None] = print,
) -> SAResult:
    """Simulated Annealing for N-Queens.

    - Neighbor: move one queen to a different row in a randomly chosen column.
    - Acceptance: always accept if H' <= H; else accept with prob exp(-(H'-H)/T).
    - Schedule: exponential (T = T0 * alpha^t) or linear.
    - Stops: H=0, temperature reaches Tmin, or max_states_evaluated consumes.
    """
    rng = random.Random(seed)
    counter = ObjectiveCounter()
    start = time.time()

    # If T0 not provided, scale with problem size
    if T0 is None:
        T0 = max(1.0, float(n))
    if schedule == "exp":
        sched = _exp_schedule(T0=T0, alpha=alpha, Tmin=Tmin)
    elif schedule == "linear":
        steps = linear_steps if linear_steps is not None else max_states_evaluated
        sched = _linear_schedule(T0=T0, steps=steps, Tmin=Tmin)
    else:
        raise ValueError("schedule must be 'exp' or 'linear'")

    if verbose:
        print_fn(
            f"[SA] Start n={n}, seed={seed}, max_states={max_states_evaluated}, schedule={schedule}, "
            f"T0={T0}, alpha={alpha}, Tmin={Tmin}, linear_steps={linear_steps}"
        )

    current = random_board(n, rng)
    current_h = h_attacking_pairs(current, counter)
    best_board = list(current)
    best_h = current_h
    history_h: List[int] = [current_h]

    t = 0
    while counter.count < max_states_evaluated and current_h > 0:
        T = sched(t)
        if verbose:
            print_fn(f"[SA][t={t}] T={T:.6f}, H={current_h}, states={counter.count}")

        neighbor = _random_neighbor(current, rng)
        nb_h = h_attacking_pairs(neighbor, counter)

        # Acceptance decision
        delta = nb_h - current_h
        accept = False
        if nb_h <= current_h:
            accept = True
        else:
            # Temperature may be zero due to Tmin clamp; avoid div-by-zero
            if T > 0:
                p = math.exp(-(delta) / T)
                accept = rng.random() < p
            else:
                accept = False

        if accept:
            current = neighbor
            current_h = nb_h
            history_h.append(current_h)
            if verbose:
                print_fn(f"[SA][t={t}] ACCEPT delta={delta}, new_H={current_h}")
            if current_h < best_h:
                best_board, best_h = list(current), current_h
        else:
            if verbose:
                print_fn(f"[SA][t={t}] REJECT delta={delta}, keep_H={current_h}")

        # Stop if temperature hit Tmin and no improvements likely
        if T <= Tmin and delta >= 0:
            # Only stop due to Tmin when we just evaluated a non-improving move
            break

        t += 1

    elapsed = time.time() - start

    # Return best found
    final_board = current if current_h <= best_h else best_board
    final_h = h_attacking_pairs(final_board, counter) if final_board is not current else current_h

    if verbose:
        status = "solution_found" if final_h == 0 else (
            "max_states_reached" if counter.count >= max_states_evaluated else "temperature_min"
        )
        print_fn(
            f"[SA][done] status={status}, final_H={final_h}, states={counter.count}, time_sec={elapsed:.6f}"
        )

    return SAResult(
        board=list(final_board),
        h=final_h,
        states_evaluated=counter.count,
        time_sec=elapsed,
        history_h=history_h,
        seed=seed,
        n=n,
    )


__all__ = ["simulated_annealing", "SAResult"]
