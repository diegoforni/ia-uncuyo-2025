import time
import random
from utils import print_solution

class NQueensCSP:
    def __init__(self, n, seed=None):
        self.n = n
        self.domains = [set(range(n)) for _ in range(n)]  # Dominios iniciales
        self.assignment = [-1] * n
        if seed is not None:
            random.seed(seed)

    def is_consistent(self, col, row):
        for prev_col in range(col):
            prev_row = self.assignment[prev_col]
            if prev_row == row or abs(prev_row - row) == abs(prev_col - col):
                return False
        return True

    def forward_check(self, col, row):
        removed = {}
        for future_col in range(col + 1, self.n):
            to_remove = set()
            for r in self.domains[future_col]:
                if r == row or abs(r - row) == abs(future_col - col):
                    to_remove.add(r)
            if to_remove:
                removed[future_col] = to_remove
                self.domains[future_col] -= to_remove
        return removed

    def restore_domains(self, removed):
        for col, values in removed.items():
            self.domains[col] |= values

    def select_unassigned_variable(self):
        unassigned = [c for c in range(self.n) if self.assignment[c] == -1]
        if not unassigned:
            return None
        return min(unassigned, key=lambda c: len(self.domains[c]))

    def order_domain_values(self, col):
        def count_conflicts(row):
            count = 0
            for future_col in range(col + 1, self.n):
                for r in self.domains[future_col]:
                    if r == row or abs(r - row) == abs(future_col - col):
                        count += 1
            return count
        return sorted(self.domains[col], key=count_conflicts)

    def backtrack(self):
        if all(a != -1 for a in self.assignment):
            return [self.assignment[:]]

        if any(len(self.domains[c]) == 0 for c in range(self.n) if self.assignment[c] == -1):
            return []

        col = self.select_unassigned_variable()
        if col is None:
            return []

        solutions = []
        for row in self.order_domain_values(col):
            self.nodes_explored += 1  # Contar cada asignación probada
            if self.is_consistent(col, row):
                self.assignment[col] = row
                removed = self.forward_check(col, row)
                result = self.backtrack()
                if result:
                    solutions.extend(result)
                self.restore_domains(removed)
                self.assignment[col] = -1
        return solutions

    def solve(self):
        self.nodes_explored = 0
        start_time = time.time()
        solutions = self.backtrack()
        end_time = time.time()
        time_taken = end_time - start_time
        return solutions, time_taken, self.nodes_explored

# Ejemplo de uso
if __name__ == "__main__":
    n = 4
    csp = NQueensCSP(n, seed=1)
    solutions, time_taken, nodes = csp.solve()
    print(f"Encontradas {len(solutions)} soluciones para n={n}")
    print(f"Tiempo: {time_taken:.4f}s, Nodos: {nodes}")
    if solutions:
        print("Primera solución:")
        print_solution(solutions[0])