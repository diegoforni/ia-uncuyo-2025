from __future__ import annotations

import argparse
from typing import Callable, List, Optional

from env_utils import create_env
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
    return 1


def cost_scenario2(a, b) -> int:
    return 10 if a[0] != b[0] else 1


def heuristic_scenario1(a, b) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristic_scenario2(a, b) -> int:
    return abs(a[1] - b[1]) * 1 + abs(a[0] - b[0]) * 10


def run_algorithm(
    grid: Grid, start, goal, algoritmo: str, limite: int, escenario: int
) -> Optional[List]:
    if algoritmo == "random":
        path, _ = random_search(grid, start, goal)
    elif algoritmo == "bfs":
        path, _ = bfs(grid, start, goal)
    elif algoritmo == "dfs":
        path, _ = dfs(grid, start, goal)
    elif algoritmo == "dls":
        path, _ = dls(grid, start, goal, limite)
    elif algoritmo == "ucs":
        cost_fn = cost_scenario1 if escenario == 1 else cost_scenario2
        path, _ = uniform_cost_search(grid, start, goal, cost_fn)
    elif algoritmo == "astar":
        if escenario == 1:
            path, _ = a_star(grid, start, goal, cost_scenario1, heuristic_scenario1)
        else:
            path, _ = a_star(grid, start, goal, cost_scenario2, heuristic_scenario2)
    else:
        raise ValueError(f"Algoritmo no soportado: {algoritmo}")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolver FrozenLake mediante búsqueda")
    parser.add_argument("--algoritmo", required=True, help="random, bfs, dfs, dls, ucs, astar")
    parser.add_argument("--escenario", type=int, choices=[1, 2], default=1)
    parser.add_argument("--limite", type=int, default=50, help="límite para DLS")
    parser.add_argument("--size", type=int, default=8)
    parser.add_argument("--p", type=float, default=0.8, help="probabilidad de hielo")
    args = parser.parse_args()

    env, desc = create_env(size=args.size, p_frozen=args.p)
    grid = desc
    start = find_tile(grid, "S")
    goal = find_tile(grid, "G")

    path = run_algorithm(grid, start, goal, args.algoritmo.lower(), args.limite, args.escenario)

    print("Entorno generado:")
    for row in grid:
        print(row)

    if path:
        print("\nCamino encontrado:")
        for state in path:
            print(state)
    else:
        print("\nNo se encontró una solución")


if __name__ == "__main__":
    main()
