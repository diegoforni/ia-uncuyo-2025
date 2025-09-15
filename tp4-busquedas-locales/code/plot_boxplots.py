import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import csv


def _read_csv_group(csv_path: Path) -> Tuple[List[int], List[str], Dict[Tuple[int, str], Dict[str, List[float]]]]:
    sizes: List[int] = []
    algos: List[str] = []
    data: Dict[Tuple[int, str], Dict[str, List[float]]] = {}
    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                size = int(row.get("size", ""))
            except Exception:
                continue
            algo = str(row.get("algorithm_name", "")).strip()
            try:
                H = float(row.get("H", "nan"))
                states = float(row.get("states", "nan"))
                t = float(row.get("time", "nan"))
            except Exception:
                continue
            key = (size, algo)
            if key not in data:
                data[key] = {"H": [], "states": [], "time": []}
            data[key]["H"].append(H)
            data[key]["states"].append(states)
            data[key]["time"].append(t)
            if size not in sizes:
                sizes.append(size)
            if algo not in algos:
                algos.append(algo)
    sizes.sort()
    return sizes, algos, data


def make_boxplots(csv_path: Path, out_dir: Path, dpi: int = 150) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    sizes, algos, grouped = _read_csv_group(csv_path)

    # Excluir RANDOM de todos los gráficos
    algos = [a for a in algos if str(a).lower() != "random"]

    # Preferred algorithm order if present
    # Orden preferido (sin RANDOM)
    algo_order = ["HC", "SA", "GA"]
    present_algos = [a for a in algo_order if a in algos]
    for a in sorted(set(algos) - set(present_algos)):
        present_algos.append(a)

    outputs: List[Path] = []
    for size in sizes:
        for metric, ylabel in [("H", "H (attacking pairs)"), ("states", "States evaluated"), ("time", "Time (s)")]:
            data = [grouped.get((size, algo), {metric: []}).get(metric, []) for algo in present_algos]

            plt.figure(figsize=(6, 4))
            bp = plt.boxplot(data, tick_labels=present_algos, patch_artist=True, showfliers=False)
            # Simple coloring
            colors = ["#4e79a7", "#f28e2c", "#59a14f", "#e15759", "#76b7b2", "#edc949"]
            for patch, c in zip(bp['boxes'], colors * 3):
                patch.set_facecolor(c)
            plt.ylabel(ylabel)
            plt.title(f"N-Queens n={int(size)} — {metric} by algorithm")
            plt.tight_layout()
            out_file = out_dir / f"boxplot_{metric}_n{int(size)}.png"
            plt.savefig(out_file, dpi=dpi)
            plt.close()
            outputs.append(out_file)

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Create boxplots for algorithms over H, states, and time")
    parser.add_argument("--csv", type=Path, default="/home/diegoforni/Documents/GitHub/ia-uncuyo-2025/tp4-busquedas-locales/tp4-Nreinas.csv", help="Input CSV produced by run_experiments.py")
    parser.add_argument("--out", type=Path, default=Path("tp4-busquedas-locales") / "images", help="Output directory for images")
    parser.add_argument("--dpi", type=int, default=150, help="Figure DPI")
    args = parser.parse_args()

    outputs = make_boxplots(args.csv, args.out, dpi=args.dpi)
    for p in outputs:
        print(p)


if __name__ == "__main__":
    main()
