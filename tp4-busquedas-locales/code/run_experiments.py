import argparse
import csv
import json
from pathlib import Path
from typing import List

try:
    from .hill_climbing import hill_climbing
    from .simulated_annealing import simulated_annealing
    from .genetic_algorithm import genetic_algorithm
    from .random_search import random_search
except ImportError:  # Allow running directly
    import os
    import sys
    sys.path.append(os.path.dirname(__file__))
    from hill_climbing import hill_climbing  # type: ignore
    from simulated_annealing import simulated_annealing  # type: ignore
    from genetic_algorithm import genetic_algorithm  # type: ignore
    from random_search import random_search  # type: ignore


def run_series(
    sizes: List[int],
    seeds: List[int],
    max_states: int,
    top_percent: float,
    out_csv: Path,
    verbose: bool = False,
    algo: str = "ALL",
    sa_schedule: str = "exp",
    sa_T0: float = 0.0,
    sa_alpha: float = 0.995,
    sa_Tmin: float = 1e-3,
    sa_linear_steps: int = 0,
    # GA parameters (optional; defaults mimic assignment-like behavior)
    ga_pop_mult: float = 7.0,
    ga_elite_frac: float = 0.5,
    ga_tournament_k: int = 0,  # 0 => auto
    ga_mutation: float = 0.0,   # 0 => auto 1/N
    ga_max_gens: int = 0,       # 0 => auto from budget
) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "algorithm_name",
                "env_n",
                "size",
                "best_solution",
                "H",
                "states",
                "time",
            ],
        )
        writer.writeheader()

        algolist = ["HC", "SA", "GA", "RANDOM"] if algo == "ALL" else [algo]
        for algoname in algolist:
            for n in sizes:
                for env_n, seed in enumerate(seeds, start=1):
                    if algoname == "HC":
                        res = hill_climbing(
                            n=n,
                            seed=seed,
                            max_states_evaluated=max_states,
                            top_percent=top_percent,
                            verbose=verbose,
                        )
                    elif algoname == "SA":
                        # if sa_T0 is 0.0, default to n
                        T0 = (float(n) if sa_T0 == 0.0 else sa_T0)
                        linear_steps = (sa_linear_steps if sa_linear_steps > 0 else max_states)
                        res = simulated_annealing(
                            n=n,
                            seed=seed,
                            max_states_evaluated=max_states,
                            schedule=sa_schedule,
                            T0=T0,
                            alpha=sa_alpha,
                            Tmin=sa_Tmin,
                            linear_steps=linear_steps,
                            verbose=verbose,
                        )
                    elif algoname == "GA":
                        res = genetic_algorithm(
                            n=n,
                            seed=seed,
                            max_states_evaluated=max_states,
                            verbose=verbose,
                            pop_mult=ga_pop_mult,
                            elite_frac=ga_elite_frac,
                            tournament_k=(None if ga_tournament_k <= 0 else ga_tournament_k),
                            mutation_prob=(None if ga_mutation <= 0.0 else ga_mutation),
                            max_generations=(None if ga_max_gens <= 0 else ga_max_gens),
                        )
                    elif algoname == "RANDOM":
                        res = random_search(
                            n=n,
                            seed=seed,
                            max_states_evaluated=max_states,
                            verbose=verbose,
                        )
                    else:
                        raise ValueError("Unsupported algo. Use 'HC', 'SA', 'GA', 'RANDOM', or 'ALL'.")
                    writer.writerow(
                        {
                            "algorithm_name": ("random" if algoname == "RANDOM" else algoname),
                            "env_n": env_n,
                            "size": n,
                            "best_solution": json.dumps(res.board),
                            "H": res.h,
                            "states": res.states_evaluated,
                            "time": f"{res.time_sec:.6f}",
                        }
                    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local search (HC/SA/GA/RANDOM/ALL) for N-Queens and export CSV")
    parser.add_argument("--sizes", type=int, nargs="*", default=[4, 8, 10], help="Board sizes to test")
    parser.add_argument("--seeds", type=int, nargs="*", default=list(range(1, 31)), help="Seeds to use")
    parser.add_argument("--max-states", type=int, default=5000, help="Max number of H evaluations")
    parser.add_argument("--top-percent", type=float, default=0.05, help="Top percent for stochastic selection (0-1)")
    parser.add_argument("--verbose", action="store_true", help="Enable step-by-step logging for the chosen algorithm")
    parser.add_argument("--algo", choices=["HC", "SA", "GA", "RANDOM", "ALL"], default="ALL", help="Algorithm(s): HC, SA, GA, RANDOM, or ALL")
    # SA parameters
    parser.add_argument("--sa-schedule", choices=["exp", "linear"], default="exp", help="SA schedule type")
    parser.add_argument("--sa-T0", type=float, default=0.0, help="Initial temperature (0 => use N)")
    parser.add_argument("--sa-alpha", type=float, default=0.995, help="Exponential decay factor for SA")
    parser.add_argument("--sa-Tmin", type=float, default=1e-3, help="Minimum temperature clamp for SA")
    parser.add_argument("--sa-linear-steps", type=int, default=0, help="Linear schedule steps (0 => use max-states)")
    # GA parameters
    parser.add_argument("--ga-pop-mult", type=float, default=7.0, help="Population size multiplier (pop = mult * N)")
    parser.add_argument("--ga-elite-frac", type=float, default=0.5, help="Elite fraction (elites = frac * N)")
    parser.add_argument("--ga-tournament-k", type=int, default=0, help="Tournament size (0 => auto)")
    parser.add_argument("--ga-mutation", type=float, default=0.0, help="Per-gene mutation probability (0 => 1/N)")
    parser.add_argument("--ga-max-gens", type=int, default=0, help="Max generations (0 => auto by budget)")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("tp4-busquedas-locales") / "tp4-Nreinas.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()

    run_series(
        sizes=args.sizes,
        seeds=args.seeds,
        max_states=args.max_states,
        top_percent=args.top_percent,
        out_csv=args.out,
        verbose=bool(args.verbose),
        algo=args.algo,
        sa_schedule=args.sa_schedule,
        sa_T0=args.sa_T0,
        sa_alpha=args.sa_alpha,
        sa_Tmin=args.sa_Tmin,
        sa_linear_steps=args.sa_linear_steps,
        ga_pop_mult=args.ga_pop_mult,
        ga_elite_frac=args.ga_elite_frac,
        ga_tournament_k=args.ga_tournament_k,
        ga_mutation=args.ga_mutation,
        ga_max_gens=args.ga_max_gens,
    )


if __name__ == "__main__":
    main()
