import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt

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


def _run_single(
    algo: str,
    n: int,
    seed: int,
    max_states: int,
    top_percent: float,
    sa_schedule: str,
    sa_T0: float,
    sa_alpha: float,
    sa_Tmin: float,
    sa_linear_steps: int,
    ga_pop_mult: float,
    ga_elite_frac: float,
    ga_tournament_k: int,
    ga_mutation: float,
    ga_max_gens: int,
    verbose: bool,
):
    if algo == "HC":
        return hill_climbing(
            n=n,
            seed=seed,
            max_states_evaluated=max_states,
            top_percent=top_percent,
            verbose=verbose,
        )
    if algo == "SA":
        T0 = (float(n) if sa_T0 == 0.0 else sa_T0)
        linear_steps = (sa_linear_steps if sa_linear_steps > 0 else max_states)
        return simulated_annealing(
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
    if algo == "GA":
        return genetic_algorithm(
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
    if algo == "RANDOM":
        return random_search(
            n=n,
            seed=seed,
            max_states_evaluated=max_states,
            verbose=verbose,
        )
    raise ValueError("Unsupported algo. Use 'HC', 'SA', 'GA', or 'RANDOM'.")


def plot_trajectories(
    algos: List[str],
    n: int,
    seed: int,
    max_states: int,
    out_dir: Path,
    dpi: int,
    top_percent: float,
    sa_schedule: str,
    sa_T0: float,
    sa_alpha: float,
    sa_Tmin: float,
    sa_linear_steps: int,
    ga_pop_mult: float,
    ga_elite_frac: float,
    ga_tournament_k: int,
    ga_mutation: float,
    ga_max_gens: int,
    verbose: bool,
) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: List[Path] = []

    # Colors for consistent legend
    color_map: Dict[str, str] = {
        "HC": "#4e79a7",
        "SA": "#f28e2c",
        "GA": "#59a14f",
        "RANDOM": "#e15759",
    }

    # Individual figures per algorithm
    for algo in algos:
        res = _run_single(
            algo=algo,
            n=n,
            seed=seed,
            max_states=max_states,
            top_percent=top_percent,
            sa_schedule=sa_schedule,
            sa_T0=sa_T0,
            sa_alpha=sa_alpha,
            sa_Tmin=sa_Tmin,
            sa_linear_steps=sa_linear_steps,
            ga_pop_mult=ga_pop_mult,
            ga_elite_frac=ga_elite_frac,
            ga_tournament_k=ga_tournament_k,
            ga_mutation=ga_mutation,
            ga_max_gens=ga_max_gens,
            verbose=verbose,
        )

        y = res.history_h
        x = list(range(len(y)))
        plt.figure(figsize=(6, 4))
        plt.plot(x, y, marker="o", ms=3, lw=1.5, color=color_map.get(algo, "#333333"))
        plt.xlabel("Iteración")
        plt.ylabel("H (pares en conflicto)")
        title = f"{algo} — N={res.n}, seed={res.seed} | H_final={res.h} | estados={res.states_evaluated} | t={res.time_sec:.3f}s"
        plt.title(title)
        plt.grid(True, alpha=0.25)
        plt.tight_layout()
        fname = out_dir / f"traj_{algo}_n{res.n}_seed{res.seed}.png"
        plt.savefig(fname, dpi=dpi)
        plt.close()
        outputs.append(fname)

    # Combined figure for quick comparison (optional convenience)
    if len(algos) > 1:
        plt.figure(figsize=(7.5, 4.5))
        for algo in algos:
            res = _run_single(
                algo=algo,
                n=n,
                seed=seed,
                max_states=max_states,
                top_percent=top_percent,
                sa_schedule=sa_schedule,
                sa_T0=sa_T0,
                sa_alpha=sa_alpha,
                sa_Tmin=sa_Tmin,
                sa_linear_steps=sa_linear_steps,
                ga_pop_mult=ga_pop_mult,
                ga_elite_frac=ga_elite_frac,
                ga_tournament_k=ga_tournament_k,
                ga_mutation=ga_mutation,
                ga_max_gens=ga_max_gens,
                verbose=False,
            )
            y = res.history_h
            x = list(range(len(y)))
            lbl = f"{algo} (H_final={res.h})"
            plt.plot(x, y, marker="o", ms=3, lw=1.5, label=lbl, color=color_map.get(algo, None))
        plt.xlabel("Iteración")
        plt.ylabel("H (pares en conflicto)")
        plt.title(f"Trayectorias H — N={n}, seed={seed}")
        plt.grid(True, alpha=0.25)
        plt.legend()
        plt.tight_layout()
        combo = out_dir / f"traj_ALL_n{n}_seed{seed}.png"
        plt.savefig(combo, dpi=dpi)
        plt.close()
        outputs.append(combo)

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Graficar H() vs iteración para una sola ejecución por algoritmo")
    parser.add_argument("--n", type=int, default=8, help="Tamaño del tablero N")
    parser.add_argument("--seed", type=int, default=1, help="Semilla RNG para reproducibilidad")
    parser.add_argument("--max-states", type=int, default=5000, help="Máx. evaluaciones de H()")
    parser.add_argument("--algo", choices=["HC", "SA", "GA", "RANDOM", "ALL"], default="ALL", help="Algoritmo(s)")
    parser.add_argument("--out", type=Path, default=Path("tp4-busquedas-locales") / "images", help="Directorio de salida")
    parser.add_argument("--dpi", type=int, default=150, help="DPI de las figuras")
    parser.add_argument("--verbose", action="store_true", help="Log detallado durante la corrida")

    # Parámetros HC
    parser.add_argument("--top-percent", type=float, default=0.05, help="Porcentaje top para selección estocástica (HC)")

    # Parámetros SA
    parser.add_argument("--sa-schedule", choices=["exp", "linear"], default="exp", help="Enfriamiento SA")
    parser.add_argument("--sa-T0", type=float, default=0.0, help="Temperatura inicial (0 => usar N)")
    parser.add_argument("--sa-alpha", type=float, default=0.995, help="Factor exponencial para SA")
    parser.add_argument("--sa-Tmin", type=float, default=1e-3, help="Temperatura mínima SA")
    parser.add_argument("--sa-linear-steps", type=int, default=0, help="Pasos lineales (0 => usar max-states)")

    # Parámetros GA
    parser.add_argument("--ga-pop-mult", type=float, default=7.0, help="Tamaño de población (mult * N)")
    parser.add_argument("--ga-elite-frac", type=float, default=0.5, help="Fracción de élites (elites = frac * N)")
    parser.add_argument("--ga-tournament-k", type=int, default=0, help="Torneo k (0 => auto)")
    parser.add_argument("--ga-mutation", type=float, default=0.0, help="Prob. mutación por gen (0 => 1/N)")
    parser.add_argument("--ga-max-gens", type=int, default=0, help="Máx. generaciones (0 => auto por presupuesto)")

    args = parser.parse_args()

    # Por requerimiento, ALL no incluye RANDOM por defecto
    algos = ["HC", "SA", "GA"] if args.algo == "ALL" else [args.algo]

    outputs = plot_trajectories(
        algos=algos,
        n=args.n,
        seed=args.seed,
        max_states=args.max_states,
        out_dir=args.out,
        dpi=args.dpi,
        top_percent=args.top_percent,
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
        verbose=bool(args.verbose),
    )

    for p in outputs:
        print(p)


if __name__ == "__main__":
    main()
