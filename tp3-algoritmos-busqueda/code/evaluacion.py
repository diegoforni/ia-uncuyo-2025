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


def cost_scenario2(a, b) -> int:
    return 10 if a[0] != b[0] else 1


def heuristic_scenario2(a, b) -> int:
    return abs(a[1] - b[1]) * 1 + abs(a[0] - b[0]) * 10


def path_cost(path: List[Tuple[int, int]]) -> Tuple[int, int]:
    if not path:
        return 0, 0
    actions = len(path) - 1
    cost = 0
    for i in range(len(path) - 1):
        cost += cost_scenario2(path[i], path[i + 1])
    return actions, cost


def run_algorithms(grid: Grid, start, goal) -> List[Dict]:
    algos = {
        "RANDOM": lambda: random_search(grid, start, goal),
        "BFS": lambda: bfs(grid, start, goal),
        "DFS": lambda: dfs(grid, start, goal),
        "DLS50": lambda: dls(grid, start, goal, 50),
        "DLS75": lambda: dls(grid, start, goal, 75),
        "DLS100": lambda: dls(grid, start, goal, 100),
        "UCS": lambda: uniform_cost_search(grid, start, goal, cost_scenario2),
        "A*": lambda: a_star(grid, start, goal, cost_scenario2, heuristic_scenario2),
    }

    records = []
    for name, func in algos.items():
        t0 = time.time()
        path, explored = func()
        elapsed = time.time() - t0
        actions, cost = path_cost(path) if path else (0, 0)
        records.append(
            {
                "algorithm_name": name,
                "states_n": explored,
                "actions_count": actions,
                "actions_cost": cost,
                "time": elapsed,
                "solution_found": bool(path),
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

    all_records = []
    for env_n in range(1, args.runs + 1):
        desc = generate_random_map_custom(args.size, args.p, seed=args.seed + env_n)
        start = find_tile(desc, "S")
        goal = find_tile(desc, "G")
        records = run_algorithms(desc, start, goal)
        for r in records:
            r["env_n"] = env_n
        all_records.extend(records)

    df = pd.DataFrame(all_records)
    df.to_csv(args.results, index=False)

    metrics = ["states_n", "actions_count", "actions_cost", "time"]
    for metric in metrics:
        plt.figure()
        sns.boxplot(data=df, x="algorithm_name", y=metric)
        plt.tight_layout()
        plt.savefig(args.images / f"{metric}.png")
        plt.close()


if __name__ == "__main__":
    main()
