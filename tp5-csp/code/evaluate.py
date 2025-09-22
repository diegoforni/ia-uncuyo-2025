import csv
import statistics
import matplotlib.pyplot as plt
from backtracking import solve_nqueens as bt_solve
from csp_nqueens import NQueensCSP

# Semillas predefinidas
seeds = list(range(1, 31))
n_values = [4, 8, 10]

# Resultados
results = []

for algo in ['backtracking', 'csp']:
    for n in n_values:
        times = []
        nodes_list = []
        found_count = 0
        for seed in seeds:
            if algo == 'backtracking':
                solutions, time_taken, nodes = bt_solve(n, seed)
            else:
                csp = NQueensCSP(n, seed)
                solutions, time_taken, nodes = csp.solve()
            
            found = 1 if solutions else 0
            found_count += found
            if found:
                times.append(time_taken)
                nodes_list.append(nodes)
            
            results.append({
                'algorithm': algo,
                'n': n,
                'seed': seed,
                'time': time_taken if found else None,
                'nodes': nodes if found else None,
                'found': found
            })
        
        # Calcular estadísticas
        success_rate = (found_count / 30) * 100
        if times:
            avg_time = statistics.mean(times)
            std_time = statistics.stdev(times) if len(times) > 1 else 0
            avg_nodes = statistics.mean(nodes_list)
            std_nodes = statistics.stdev(nodes_list) if len(nodes_list) > 1 else 0
        else:
            avg_time = std_time = avg_nodes = std_nodes = 0
        
        print(f"{algo} n={n}: Success {success_rate}%, Avg Time {avg_time:.4f}s ± {std_time:.4f}, Avg Nodes {avg_nodes:.0f} ± {std_nodes:.0f}")

# Guardar CSV
with open('results.csv', 'w', newline='') as csvfile:
    fieldnames = ['algorithm', 'n', 'seed', 'time', 'nodes', 'found']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

# Boxplots
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# Tiempos
data_times = {}
for algo in ['backtracking', 'csp']:
    for n in n_values:
        key = f"{algo}_n{n}"
        data_times[key] = [r['time'] for r in results if r['algorithm'] == algo and r['n'] == n and r['found']]

axes[0].boxplot(data_times.values(), labels=data_times.keys())
axes[0].set_title('Distribución de Tiempos de Ejecución')
axes[0].set_ylabel('Tiempo (s)')

# Nodos
data_nodes = {}
for algo in ['backtracking', 'csp']:
    for n in n_values:
        key = f"{algo}_n{n}"
        data_nodes[key] = [r['nodes'] for r in results if r['algorithm'] == algo and r['n'] == n and r['found']]

axes[1].boxplot(data_nodes.values(), labels=data_nodes.keys())
axes[1].set_title('Distribución de Nodos Explorados')
axes[1].set_ylabel('Nodos')

plt.tight_layout()
plt.savefig('boxplots.png')
plt.show()
