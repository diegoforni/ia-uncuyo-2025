import random
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple, Callable

try:
    from .nqueens import (
        Board,
        ObjectiveCounter,
        random_board,
        h_attacking_pairs,
        generate_neighbors,
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
        generate_neighbors,
        apply_move,
    )


@dataclass
class HCResult:
    board: Board
    h: int
    states_evaluated: int
    time_sec: float
    history_h: List[int]
    seed: int
    n: int


def _select_top_stochastic(
    neighbor_evals: List[Tuple[Board, int]],
    top_percent: float,
    rng: random.Random,
) -> Board:
    """Select a neighbor from top X% by H, with probability proportional to score.

    Lower H is better. Weights are computed to favor lower H among the top group.
    neighbor_evals: list of (board, h) sorted ASC by h before calling.
    """
    k = max(1, int(round(len(neighbor_evals) * top_percent)))
    top_group = neighbor_evals[:k]
    # Weight: higher when h is lower. Ensure positivity in case of ties
    best_h = top_group[0][1]
    weights = [(best_h - h + 1) for (_, h) in top_group]
    total_w = sum(weights)
    # Fallback to uniform if numerical issues
    if total_w <= 0:
        idx = rng.randrange(len(top_group))
        return top_group[idx][0]
    r = rng.random() * total_w
    acc = 0.0
    for (b, h), w in zip(top_group, weights):
        acc += w
        if r <= acc:
            return b
    # Numerical edge: return last
    return top_group[-1][0]


def hill_climbing(
    n: int,
    seed: int,
    max_states_evaluated: int,
    top_percent: float = 0.05,
    verbose: bool = False,
    print_fn: Callable[[str], None] = print,
) -> HCResult:
    """Canonical Hill Climbing for N-Queens with top-5% stochastic neighbor policy.

    - Representation: list of length n, board[c] = row of queen in column c.
    - Objective: H(board) = number of attacking pairs (lower is better).
    - Move: change the row of one queen (one column).
    - Policy: among improving neighbors, pick randomly from the top X% by H,
      with probability proportional to a decreasing function of H.
    - Stops: when no improving neighbor exists or max_states_evaluated is reached.
    """
    rng = random.Random(seed)
    counter = ObjectiveCounter()
    start = time.time()

    if verbose:
        print_fn(f"[HC] Start n={n}, seed={seed}, max_states={max_states_evaluated}, top_percent={top_percent}")

    current = random_board(n, rng)
    current_h = h_attacking_pairs(current, counter)
    if verbose:
        print_fn(f"[HC] Initial board: {current} | H={current_h}")

    best_board = list(current)
    best_h = current_h
    history_h: List[int] = [current_h]

    # Main loop
    iteration = 0
    while counter.count < max_states_evaluated and current_h > 0:
        iteration += 1
        if verbose:
            print_fn(f"[HC][it={iteration}] Current H={current_h}, states_evaluated={counter.count}")
        neighbors = generate_neighbors(current)

        # Evaluate neighbors one by one to respect max_states_evaluated
        improving: List[Tuple[Board, int]] = []  # (board, h)
        evaluated_this_step = 0
        for mv in neighbors:
            if counter.count >= max_states_evaluated:
                break
            nb = apply_move(current, mv)
            nb_h = h_attacking_pairs(nb, counter)
            evaluated_this_step += 1
            if nb_h < current_h:
                improving.append((nb, nb_h))
            # Track global best seen
            if nb_h < best_h:
                best_board, best_h = nb, nb_h
        if verbose:
            print_fn(
                f"[HC][it={iteration}] Evaluated neighbors: {evaluated_this_step}, improving: {len(improving)}, best_seen_H={best_h}"
            )

        if not improving:
            if verbose:
                reason = "max_states_reached" if counter.count >= max_states_evaluated else "no_improving_neighbors"
                print_fn(f"[HC][stop] {reason}: current_H={current_h}, states={counter.count}")
            break  # Local minimum/plateau reached

        # Sort improving neighbors by h ascending
        improving.sort(key=lambda x: x[1])

        # Choose one from top_percent
        k = max(1, int(round(len(improving) * top_percent)))
        if verbose:
            h_values = [h for _, h in improving[:k]]
            if h_values:
                print_fn(
                    f"[HC][it={iteration}] Selecting from top {k}/{len(improving)}; H-range=[{min(h_values)},{max(h_values)}]"
                )
        next_board = _select_top_stochastic(improving, top_percent, rng)
        current = next_board
        current_h = h_attacking_pairs(current, counter)  # count this eval as well
        history_h.append(current_h)
        if verbose:
            print_fn(
                f"[HC][it={iteration}] Moved. New H={current_h}, states_evaluated={counter.count}"
            )
        if current_h < best_h:
            best_board, best_h = list(current), current_h

    elapsed = time.time() - start

    # If we stopped due to max_states, return best found so far
    final_board = current if (current_h == 0 or current_h <= best_h) else best_board
    final_h = h_attacking_pairs(final_board, counter) if final_board is not current else current_h

    if verbose:
        status = "solution_found" if final_h == 0 else (
            "max_states_reached" if counter.count >= max_states_evaluated else "local_minimum"
        )
        print_fn(
            f"[HC][done] status={status}, final_H={final_h}, states={counter.count}, time_sec={elapsed:.6f}"
        )

    return HCResult(
        board=list(final_board),
        h=final_h,
        states_evaluated=counter.count,
        time_sec=elapsed,
        history_h=history_h,
        seed=seed,
        n=n,
    )


__all__ = ["hill_climbing", "HCResult"]
