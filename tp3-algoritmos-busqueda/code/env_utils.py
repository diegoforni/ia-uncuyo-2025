import random
from typing import List, Tuple, Sequence

import gymnasium as gym
from gymnasium import wrappers


def generate_random_map_custom(
    size: int,
    p_frozen: float = 0.92,
    seed: int | None = None,
) -> List[str]:
    """Generate a random FrozenLake map with random start and goal positions.

    Args:
        size: side length of the square grid.
        p_frozen: probability for each tile to be frozen ("F").
        seed: optional seed for reproducibility.

    Returns:
        A list of strings representing the map description accepted by
        ``gymnasium.make``.
    """
    rng = random.Random(seed)

    def random_cell() -> str:
        return "F" if rng.random() < p_frozen else "H"

    grid = [[random_cell() for _ in range(size)] for _ in range(size)]
    start = (rng.randrange(size), rng.randrange(size))
    goal = (rng.randrange(size), rng.randrange(size))
    while goal == start:
        goal = (rng.randrange(size), rng.randrange(size))

    grid[start[0]][start[1]] = "S"
    grid[goal[0]][goal[1]] = "G"

    return ["".join(row) for row in grid]


def create_env(
    size: int = 100,
    p_frozen: float = 0.92,
    max_steps: int = 1000,
    is_slippery: bool = False,
    seed: int | None = None,
    render_mode: str | None = None,
):
    """Create a FrozenLake environment with given parameters.

    Returns the environment and the map description used to create it.
    """
    desc = generate_random_map_custom(size=size, p_frozen=p_frozen, seed=seed)
    env = gym.make(
        "FrozenLake-v1", desc=desc, is_slippery=is_slippery, render_mode=render_mode
    )
    env = wrappers.TimeLimit(env.env, max_steps)
    return env, desc
