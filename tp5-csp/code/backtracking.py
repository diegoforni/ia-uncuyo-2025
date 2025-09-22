import time
import random
from utils import is_safe, print_solution

def solve_nqueens(n, seed=None):
    """
    Resuelve el problema de N-Reinas usando backtracking con LCV (sin MRV).
    Retorna (solutions, time_taken, nodes_explored)
    """
    if seed is not None:
        random.seed(seed)
    
    domains = [set(range(n)) for _ in range(n)]  # Dominios estáticos para LCV
    
    def order_domain_values(col):
        """LCV: Ordena filas por menor impacto en futuras columnas."""
        def count_conflicts(row):
            count = 0
            for future_col in range(col + 1, n):
                for r in domains[future_col]:
                    if r == row or abs(r - row) == abs(future_col - col):
                        count += 1
            return count
        return sorted(domains[col], key=count_conflicts)
    
    nodes_explored = 0
    
    def backtrack(board, col):
        nonlocal nodes_explored
        if col == n:
            return [board[:]]  # Solución encontrada
        solutions = []
        for row in order_domain_values(col):  # Usar LCV
            nodes_explored += 1  # Contar cada asignación probada
            board[col] = row
            if is_safe(board, col):
                result = backtrack(board, col + 1)
                if result:
                    solutions.extend(result)
        return solutions
    
    start_time = time.time()
    solutions = []
    board = [-1] * n
    solutions = backtrack(board, 0)
    end_time = time.time()
    time_taken = end_time - start_time
    
    return solutions, time_taken, nodes_explored

# Ejemplo de uso (para pruebas individuales)
if __name__ == "__main__":
    n = 4
    solutions, time_taken, nodes = solve_nqueens(n, seed=1)
    print(f"Encontradas {len(solutions)} soluciones para n={n}")
    print(f"Tiempo: {time_taken:.4f}s, Nodos: {nodes}")
    if solutions:
        print("Primera solución:")
        print_solution(solutions[0])