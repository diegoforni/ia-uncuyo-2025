from __future__ import annotations

import argparse
import random
from typing import List, Tuple

from search_algorithms import Grid, find_tile, random_search


def load_env(path: str) -> List[str]:
    """Load a saved environment description from ``path``."""
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def parse_path(path_file: str) -> List[Tuple[int, int]]:
    with open(path_file) as f:
        return [tuple(map(int, line.strip().split(","))) for line in f if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect random-walk behaviour on a saved environment."
    )
    parser.add_argument("env_file", help="Path to the environment text file")
    parser.add_argument("--path_file", help="Load an existing path for inspection")
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducibility")
    parser.add_argument(
        "--max_steps", type=int, default=1000, help="Maximum steps for random search"
    )
    parser.add_argument("--save_path", help="Where to store the generated path")
    args = parser.parse_args()

    grid: Grid = load_env(args.env_file)
    start = find_tile(grid, "S")
    goal = find_tile(grid, "G")

    if args.path_file:
        path = parse_path(args.path_file)
        explored = len(set(path))
    else:
        if args.seed is not None:
            random.seed(args.seed)
        path, explored = random_search(
            grid, start, goal, max_steps=args.max_steps, return_full_path=True
        )
        if args.save_path:
            with open(args.save_path, "w") as f:
                for r, c in path:
                    f.write(f"{r},{c}\n")

    print("Environment:")
    for row in grid:
        print(row)

    print(f"\nStart: {start} Goal: {goal}")
    print(f"Explored states: {explored}")

    tile = grid[path[-1][0]][path[-1][1]] if path else "?"
    if tile == "G":
        reason = "goal"
    elif tile == "H":
        reason = "hole"
    else:
        reason = "step limit"
    print(f"Termination reason: {reason}")

    print("Path:")
    for i, pos in enumerate(path):
        tile = grid[pos[0]][pos[1]]
        print(f"{i}: {pos} ({tile})")


if __name__ == "__main__":
    main()

