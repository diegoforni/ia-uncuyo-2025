import random
import math
import time
from dataclasses import dataclass
from typing import List, Tuple, Callable, Optional

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
class GAResult:
    board: Board
    h: int
    states_evaluated: int
    time_sec: float
    history_h: List[int]
    seed: int
    n: int


def _tournament_select(
    population: List[Tuple[Board, int]],
    rng: random.Random,
    k: int = 3,
) -> Board:
    """Pick one parent via k-way tournament (lower H wins)."""
    contestants = [population[rng.randrange(len(population))] for _ in range(k)]
    contestants.sort(key=lambda x: x[1])
    return list(contestants[0][0])


def _one_point_crossover(a: Board, b: Board, rng: random.Random) -> Tuple[Board, Board]:
    n = len(a)
    if n <= 1:
        return list(a), list(b)
    cut = rng.randrange(1, n)  # [1, n-1]
    c1 = a[:cut] + b[cut:]
    c2 = b[:cut] + a[cut:]
    return c1, c2

def _two_point_crossover(a: Board, b: Board, rng: random.Random) -> Tuple[Board, Board]:
    n = len(a)
    if n <= 2:
        return _one_point_crossover(a, b, rng)
    i = rng.randrange(0, n - 1)
    j = rng.randrange(i + 1, n)
    c1 = a[:i] + b[i:j] + a[j:]
    c2 = b[:i] + a[i:j] + b[j:]
    return c1, c2

def _uniform_crossover(a: Board, b: Board, rng: random.Random, swap_prob: float = 0.5) -> Tuple[Board, Board]:
    n = len(a)
    if n == 0:
        return [], []
    c1 = list(a)
    c2 = list(b)
    for i in range(n):
        if rng.random() < swap_prob:
            c1[i] = b[i]
        # independent mask for c2 to increase variability
        if rng.random() < swap_prob:
            c2[i] = a[i]
    return c1, c2


# Permutation-based utilities (for GA on N-Queens)
def _random_perm_board(n: int, rng: random.Random) -> Board:
    arr = list(range(n))
    rng.shuffle(arr)
    return arr


def _order_crossover(a: Board, b: Board, rng: random.Random) -> Tuple[Board, Board]:
    n = len(a)
    if n <= 1:
        return list(a), list(b)
    i = rng.randrange(0, n - 1)
    j = rng.randrange(i + 1, n)
    def ox(p1: Board, p2: Board) -> Board:
        child = [None] * n  # type: ignore
        # copy slice from p1
        child[i:j] = p1[i:j]
        used = set(p1[i:j])
        # fill remaining from p2 in order
        pos = 0
        for x in p2:
            if x in used:
                continue
            while i <= pos < j:
                pos = j
            if pos >= n:
                # wrap if needed (shouldn't happen with above step, but safe guard)
                # find first None
                pos = child.index(None)  # type: ignore
            child[pos] = x  # type: ignore
            pos += 1
        # type: ignore because we know it's fully filled
        return child  # type: ignore
    return ox(a, b), ox(b, a)


def _mutate_perm(board: Board, rng: random.Random, mut_prob: float) -> None:
    n = len(board)
    for i in range(n):
        if rng.random() < mut_prob:
            j = rng.randrange(n)
            if j == i and n > 1:
                j = (j + 1) % n
            board[i], board[j] = board[j], board[i]


def _sample_nonzero_delta(rng: random.Random, p: float = 0.7) -> int:
    """Sample a non-zero integer with two-sided geometric distribution.

    P(|k|=m) = p * (1-p)^(m-1) for m >= 1, sign chosen uniformly.
    """
    # geometric(m>=1) with parameter p
    # simulate by counting failures until first success
    m = 1
    while rng.random() > p:
        m += 1
    sign = -1 if rng.random() < 0.5 else 1
    return sign * m


def _mutate(board: Board, rng: random.Random, mut_prob: float) -> None:
    n = len(board)
    for i in range(n):
        if rng.random() < mut_prob:
            old = board[i]
            # sample until an actual change occurs after clipping
            for _ in range(10):
                delta = _sample_nonzero_delta(rng)
                new_val = old + delta
                if new_val < 0:
                    new_val = 0
                elif new_val >= n:
                    new_val = n - 1
                if new_val != old:
                    board[i] = new_val
                    break


def genetic_algorithm(
    n: int,
    seed: int,
    max_states_evaluated: int,
    verbose: bool = False,
    print_fn: Callable[[str], None] = print,
    pop_mult: float = 7.0,
    elite_frac: float = 0.5,
    tournament_k: Optional[int] = None,
    mutation_prob: Optional[float] = None,
    max_generations: Optional[int] = None,
    perm_repr: bool = True,
) -> GAResult:
    """Genetic Algorithm for N-Queens with fair-by-budget defaults.

    - Uses an automatically computed generation cap so that total H evaluations
      stay within `max_states_evaluated` (fair across algorithms).
    - Exposes knobs (population multiplier, elite fraction, tournament k, mutation,
      max generations) but keeps assignment-like defaults if not provided.
    - Fixes wasted evaluations: elites reuse cached fitness; not re-evaluated.
    """
    rng = random.Random(seed)
    counter = ObjectiveCounter()
    start = time.time()

    pop_size = max(2, int(round(pop_mult * n)))
    elite_count = max(1, int(round(elite_frac * n)))
    # Selection pressure scales with population size (and thus with N)
    # Default tournament size: log2(pop) clamped [2, 7] if not provided
    if tournament_k is None or tournament_k <= 0:
        t_k = max(2, min(7, int(round(math.log2(pop_size)))))
    else:
        t_k = int(tournament_k)
    # Standard GA heuristic: expected ~1 mutated gene per individual by default
    mut_prob = (1.0 / float(n) if n > 0 else 1.0) if (mutation_prob is None or mutation_prob <= 0) else float(mutation_prob)
    # Auto generation cap: honor overall budget
    # Total evals ≈ pop_size (init) + generations * (pop_size - elite_count)
    needed_per_gen = max(1, pop_size - elite_count)
    if max_states_evaluated > pop_size:
        auto_gens = max(1, (max_states_evaluated - pop_size) // needed_per_gen)
    else:
        auto_gens = 1
    gen_cap = auto_gens if (max_generations is None or max_generations <= 0) else int(max_generations)

    if verbose:
        print_fn(
            f"[GA] Start n={n}, seed={seed}, max_states={max_states_evaluated}, pop={pop_size}, "
            f"elites={elite_count}, k={t_k}, mut_prob={mut_prob:.4f}, max_gens={gen_cap}, perm={perm_repr}"
        )

    # Initialize population and evaluate
    population: List[Tuple[Board, int]] = []
    best_board: Board
    best_h: int = 10**9
    for _ in range(pop_size):
        b = _random_perm_board(n, rng) if perm_repr else random_board(n, rng)
        h = h_attacking_pairs(b, counter)
        population.append((b, h))
        if h < best_h:
            best_board, best_h = list(b), h
    population.sort(key=lambda x: x[1])

    history_h: List[int] = [best_h]
    if verbose:
        print_fn(f"[GA][gen=0] best_H={best_h}, states={counter.count}")
    if best_h == 0 or counter.count >= max_states_evaluated:
        elapsed = time.time() - start
        return GAResult(
            board=list(best_board),
            h=best_h,
            states_evaluated=counter.count,
            time_sec=elapsed,
            history_h=history_h,
            seed=seed,
            n=n,
        )

    # Main evolution loop
    generation = 0
    while True:
        generation += 1
        if generation > gen_cap:
            if verbose:
                print_fn(f"[GA][stop] generations limit reached: {generation} > {gen_cap}")
            break
        if counter.count >= max_states_evaluated:
            if verbose:
                print_fn(f"[GA][stop] max_states reached: {counter.count}")
            break

        # Elitism: carry top elite_count
        population.sort(key=lambda x: x[1])
        elites = [list(b) for (b, _) in population[:elite_count]]

        # Early exit if best is solution
        if population[0][1] == 0:
            best_board, best_h = list(population[0][0]), 0
            history_h.append(0)
            break

        # Generate offspring to refill population
        offspring: List[Board] = []
        # Fill remaining slots
        needed = pop_size - elite_count
        while len(offspring) < needed and counter.count < max_states_evaluated:
            p1 = _tournament_select(population, rng, k=t_k)
            p2 = _tournament_select(population, rng, k=t_k)
            if perm_repr:
                c1, c2 = _order_crossover(p1, p2, rng)
                _mutate_perm(c1, rng, mut_prob)
                _mutate_perm(c2, rng, mut_prob)
            else:
                c1, c2 = _uniform_crossover(p1, p2, rng)
                _mutate(c1, rng, mut_prob)
                _mutate(c2, rng, mut_prob)
            offspring.append(c1)
            if len(offspring) < needed:
                offspring.append(c2)

        # Evaluate offspring (respect max_states)
        evaluated: List[Tuple[Board, int]] = []
        for b in offspring:
            if counter.count >= max_states_evaluated:
                break
            h = h_attacking_pairs(b, counter)
            evaluated.append((b, h))
            if h < best_h:
                best_board, best_h = list(b), h

        # Build new population using cached elite fitness (do not re-evaluate elites)
        new_population: List[Tuple[Board, int]] = population[:elite_count]
        new_population.extend(evaluated)

        # If no offspring were evaluated due to states limit, stop
        if len(evaluated) == 0 and counter.count >= max_states_evaluated:
            if verbose:
                print_fn("[GA][stop] No room to evaluate offspring before max_states")
            population = new_population
            break

        population = new_population
        population.sort(key=lambda x: x[1])
        current_best_h = population[0][1]
        if current_best_h < best_h:
            best_h = current_best_h
            best_board = list(population[0][0])
        history_h.append(best_h)
        if verbose:
            print_fn(f"[GA][gen={generation}] best_H={best_h}, states={counter.count}")

        if best_h == 0:
            break

    elapsed = time.time() - start
    final_board = list(best_board)
    final_h = best_h
    return GAResult(
        board=final_board,
        h=final_h,
        states_evaluated=counter.count,
        time_sec=elapsed,
        history_h=history_h,
        seed=seed,
        n=n,
    )


__all__ = ["genetic_algorithm", "GAResult"]
