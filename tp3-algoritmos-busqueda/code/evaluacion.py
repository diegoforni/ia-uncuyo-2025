from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from env_utils import generate_random_map_custom
from search_algorithms import (
    Grid,
    a_star,
    bfs,
    dfs,
    dls,
    find_tile,
    random_search,
    uniform_cost_search,
)


def cost_scenario1(_a, _b) -> int:
    """Cost function for scenario 1 (all moves cost 1)."""
    return 1


def cost_scenario2(a, b) -> int:
    """Cost function for scenario 2 (vertical moves cost 10)."""
    return 10 if a[0] != b[0] else 1


def heuristic_scenario1(a, b) -> int:
    """Manhattan distance for scenario 1."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristic_scenario2(a, b) -> int:
    """Admissible heuristic for scenario 2 (weighted Manhattan)."""
    return abs(a[1] - b[1]) * 1 + abs(a[0] - b[0]) * 10


def path_cost(path: List[Tuple[int, int]], cost_fn) -> Tuple[int, int]:
    """Return step count and cost according to ``cost_fn`` for the path."""
    if not path:
        return 0, 0
    actions = len(path) - 1
    cost = 0
    for i in range(len(path) - 1):
        cost += cost_fn(path[i], path[i + 1])
    return actions, cost


def run_algorithms(grid: Grid, start, goal, scenario: int) -> List[Dict]:
    """Run all algorithms for the given scenario."""
    if scenario == 1:
        cost_fn = cost_scenario1
        heuristic = heuristic_scenario1
    else:
        cost_fn = cost_scenario2
        heuristic = heuristic_scenario2

    algos = {
        "RANDOM": lambda: random_search(grid, start, goal),
        "BFS": lambda: bfs(grid, start, goal),
        "DFS": lambda: dfs(grid, start, goal),
        "DLS50": lambda: dls(grid, start, goal, 50),
        "DLS75": lambda: dls(grid, start, goal, 75),
        "DLS100": lambda: dls(grid, start, goal, 100),
        "UCS": lambda: uniform_cost_search(grid, start, goal, cost_fn),
        "A*": lambda: a_star(grid, start, goal, cost_fn, heuristic),
    }

    records: List[Dict] = []
    for name, func in algos.items():
        t0 = time.time()
        path, explored = func()
        elapsed = time.time() - t0
        actions, cost = path_cost(path, cost_fn) if path else (0, 0)
        records.append(
            {
                "algorithm_name": name,
                "states_n": explored,
                "actions_count": actions,
                "actions_cost": cost,
                "time": elapsed,
                "solution_found": bool(path),
                "scenario": scenario,
            }
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluar algoritmos de búsqueda")
    parser.add_argument("--runs", type=int, default=30)
    parser.add_argument("--size", type=int, default=100)
    parser.add_argument("--p", type=float, default=0.92)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--results", type=Path, default=Path("results.csv"))
    parser.add_argument("--images", type=Path, default=Path("images"))
    args = parser.parse_args()

    args.images.mkdir(parents=True, exist_ok=True)

    all_records: List[Dict] = []
    for env_n in range(1, args.runs + 1):
        desc = generate_random_map_custom(args.size, args.p, seed=args.seed + env_n)
        start = find_tile(desc, "S")
        goal = find_tile(desc, "G")
        for scenario in (1, 2):
            records = run_algorithms(desc, start, goal, scenario)
            for r in records:
                r["env_n"] = env_n
            all_records.extend(records)

    columns = [
        "algorithm_name",
        "env_n",
        "states_n",
        "actions_count",
        "actions_cost",
        "time",
        "solution_found",
        "scenario",
    ]
    df = pd.DataFrame(all_records)[columns]
    df.to_csv(args.results, index=False)

    metrics = ["states_n", "actions_count", "actions_cost", "time"]
    for scenario in (1, 2):
        df_s = df[df["scenario"] == scenario]
        for metric in metrics:
            plt.figure()
            sns.boxplot(data=df_s, x="algorithm_name", y=metric)
            plt.title(f"Escenario {scenario}")
            plt.tight_layout()
            plt.savefig(args.images / f"{metric}_s{scenario}.png")
            plt.close()


if __name__ == "__main__":
    main()
