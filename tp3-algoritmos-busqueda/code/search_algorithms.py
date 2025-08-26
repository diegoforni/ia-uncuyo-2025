from __future__ import annotations

import heapq
import random
from collections import deque
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

Position = Tuple[int, int]
Grid = Sequence[str]


@dataclass
class Node:
    position: Position
    parent: Optional["Node"]
    action: Optional[int]
    cost: int = 0
    depth: int = 0


# Movements: 0-left, 1-down, 2-right, 3-up as in FrozenLake
MOVES = {
    0: (0, -1),
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0),
}


def find_tile(grid: Grid, tile: str) -> Position:
    for r, row in enumerate(grid):
        c = row.find(tile)
        if c != -1:
            return r, c
    raise ValueError(f"tile {tile!r} not found")


def in_bounds(grid: Grid, pos: Position) -> bool:
    n = len(grid)
    return 0 <= pos[0] < n and 0 <= pos[1] < n


def is_passable(grid: Grid, pos: Position) -> bool:
    return grid[pos[0]][pos[1]] != "H"


def neighbors(grid: Grid, pos: Position) -> Iterable[Tuple[Position, int]]:
    for action, (dr, dc) in MOVES.items():
        new_pos = (pos[0] + dr, pos[1] + dc)
        if in_bounds(grid, new_pos) and is_passable(grid, new_pos):
            yield new_pos, action


def reconstruct_path(node: Node) -> List[Position]:
    path = []
    while node:
        path.append(node.position)
        node = node.parent
    return list(reversed(path))


def random_search(
    grid: Grid,
    start: Position,
    goal: Position,
    max_steps: int = 1000,
    return_full_path: bool = False,
) -> Tuple[Optional[List[Position]], int]:
    """Perform a random walk that can fall into holes.

    If ``return_full_path`` is ``True`` the full sequence of visited states is
    returned even when the walk ends in failure. Otherwise ``None`` is returned
    when the agent does not reach the goal.
    """
    pos = start
    path = [pos]
    explored = {pos}
    for _ in range(max_steps):
        if pos == goal:
            return path, len(explored)
        moves = []
        for dr, dc in MOVES.values():
            new_pos = (pos[0] + dr, pos[1] + dc)
            if in_bounds(grid, new_pos):
                moves.append(new_pos)
        if not moves:
            return (path if return_full_path else None), len(explored)
        pos = random.choice(moves)
        path.append(pos)
        explored.add(pos)
        tile = grid[pos[0]][pos[1]]
        if tile == "H":
            return (path if return_full_path else None), len(explored)
        if pos == goal:
            return path, len(explored)
    return (path if return_full_path else None), len(explored)


def bfs(grid: Grid, start: Position, goal: Position) -> Tuple[Optional[List[Position]], int]:
    frontier = deque([Node(start, None, None)])
    visited = {start}
    explored = 0
    while frontier:
        node = frontier.popleft()
        explored += 1
        if node.position == goal:
            return reconstruct_path(node), explored
        for new_pos, action in neighbors(grid, node.position):
            if new_pos not in visited:
                visited.add(new_pos)
                frontier.append(Node(new_pos, node, action))
    return None, explored


def dfs(grid: Grid, start: Position, goal: Position) -> Tuple[Optional[List[Position]], int]:
    stack = [Node(start, None, None)]
    visited = set()
    explored = 0
    while stack:
        node = stack.pop()
        if node.position in visited:
            continue
        visited.add(node.position)
        explored += 1
        if node.position == goal:
            return reconstruct_path(node), explored
        for new_pos, action in reversed(list(neighbors(grid, node.position))):
            if new_pos not in visited:
                stack.append(Node(new_pos, node, action))
    return None, explored


def dls(grid: Grid, start: Position, goal: Position, limit: int) -> Tuple[Optional[List[Position]], int]:
    explored = 0
    visited: set[Position] = set()

    def recursive(node: Node) -> Optional[Node]:
        nonlocal explored
        explored += 1
        visited.add(node.position)
        if node.position == goal:
            return node
        if node.depth == limit:
            return None
        for new_pos, action in neighbors(grid, node.position):
            if new_pos not in visited:
                child = Node(new_pos, node, action, depth=node.depth + 1)
                result = recursive(child)
                if result is not None:
                    return result
        return None

    result = recursive(Node(start, None, None))
    return (reconstruct_path(result) if result else None), explored


def uniform_cost_search(
    grid: Grid,
    start: Position,
    goal: Position,
    cost_fn: Callable[[Position, Position], int],
) -> Tuple[Optional[List[Position]], int]:
    frontier: List[Tuple[int, int, Node]] = []
    counter = 0
    heapq.heappush(frontier, (0, counter, Node(start, None, None)))
    visited: Dict[Position, int] = {start: 0}
    explored = 0

    while frontier:
        cost, _, node = heapq.heappop(frontier)
        explored += 1
        if node.position == goal:
            node.cost = cost
            return reconstruct_path(node), explored
        for new_pos, action in neighbors(grid, node.position):
            new_cost = cost + cost_fn(node.position, new_pos)
            if new_pos not in visited or new_cost < visited[new_pos]:
                visited[new_pos] = new_cost
                counter += 1
                heapq.heappush(
                    frontier, (new_cost, counter, Node(new_pos, node, action))
                )
    return None, explored


def a_star(
    grid: Grid,
    start: Position,
    goal: Position,
    cost_fn: Callable[[Position, Position], int],
    heuristic: Callable[[Position, Position], int],
) -> Tuple[Optional[List[Position]], int]:
    frontier: List[Tuple[int, int, Node]] = []
    counter = 0
    start_h = heuristic(start, goal)
    heapq.heappush(frontier, (start_h, counter, Node(start, None, None, cost=0)))
    visited: Dict[Position, int] = {start: 0}
    explored = 0

    while frontier:
        f, _, node = heapq.heappop(frontier)
        explored += 1
        if node.position == goal:
            return reconstruct_path(node), explored
        for new_pos, action in neighbors(grid, node.position):
            g = node.cost + cost_fn(node.position, new_pos)
            if new_pos not in visited or g < visited[new_pos]:
                visited[new_pos] = g
                counter += 1
                heapq.heappush(
                    frontier,
                    (g + heuristic(new_pos, goal), counter, Node(new_pos, node, action, g)),
                )
    return None, explored
