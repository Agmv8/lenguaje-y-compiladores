"""
Genera las graficas comparativas de rendimiento a partir de los CSV
producidos por benchmark.py.

Uso:
    python3 generate_charts.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

COLORS = {"Python": "#3776AB", "Java": "#E76F00", "Rust": "#DE3F24"}


def chart_avg_by_language(summary: pd.DataFrame):
    """Barras: tiempo promedio general por lenguaje (todos los archivos)."""
    avg_by_lang = summary.groupby("lenguaje")["tiempo_promedio_s"].mean() * 1000

    fig, ax = plt.subplots(figsize=(7, 5))
    langs = avg_by_lang.index.tolist()
    values = avg_by_lang.values
    colors = [COLORS.get(l, "#888888") for l in langs]

    bars = ax.bar(langs, values, color=colors)
    ax.set_ylabel("Tiempo promedio (ms)")
    ax.set_title("Tiempo promedio de parseo por lenguaje/herramienta\n(promedio sobre los 12 archivos de prueba)")
    ax.bar_label(bars, fmt="%.2f ms")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "chart_avg_by_language.png", dpi=150)
    plt.close(fig)


def chart_by_file(summary: pd.DataFrame):
    """Barras agrupadas: tiempo promedio por archivo, por lenguaje."""
    pivot = summary.pivot(index="archivo", columns="lenguaje", values="tiempo_promedio_s") * 1000
    pivot = pivot.sort_index()

    fig, ax = plt.subplots(figsize=(13, 6))
    pivot.plot(kind="bar", ax=ax, color=[COLORS.get(c, "#888") for c in pivot.columns])
    ax.set_ylabel("Tiempo promedio (ms)")
    ax.set_xlabel("Archivo de prueba")
    ax.set_title("Tiempo de parseo por archivo, comparado entre lenguajes/herramientas")
    ax.legend(title="Lenguaje")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=45, ha="right")

    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "chart_by_file.png", dpi=150)
    plt.close(fig)


def chart_vs_size(summary: pd.DataFrame):
    """Dispersion: tiempo promedio vs tamano del archivo (lineas), por lenguaje."""
    fig, ax = plt.subplots(figsize=(8, 6))

    for lang, group in summary.groupby("lenguaje"):
        group_sorted = group.sort_values("lineas")
        ax.plot(
            group_sorted["lineas"],
            group_sorted["tiempo_promedio_s"] * 1000,
            marker="o",
            label=lang,
            color=COLORS.get(lang, "#888888"),
        )

    ax.set_xlabel("Tamano del archivo (numero de lineas)")
    ax.set_ylabel("Tiempo promedio (ms)")
    ax.set_title("Tiempo de parseo vs. tamano del archivo")
    ax.legend(title="Lenguaje")
    ax.grid(linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "chart_time_vs_size.png", dpi=150)
    plt.close(fig)


def chart_boxplot(raw: pd.DataFrame):
    """Boxplot: distribucion de tiempos por lenguaje (variabilidad entre corridas)."""
    fig, ax = plt.subplots(figsize=(7, 5))
    langs = ["Python", "Java", "Rust"]
    data = [raw[raw["lenguaje"] == l]["tiempo_segundos"] * 1000 for l in langs]

    box = ax.boxplot(data, tick_labels=langs, patch_artist=True)
    for patch, lang in zip(box["boxes"], langs):
        patch.set_facecolor(COLORS.get(lang, "#888888"))
        patch.set_alpha(0.7)

    ax.set_ylabel("Tiempo (ms)")
    ax.set_title("Distribucion de tiempos de ejecucion por lenguaje\n(todas las corridas, todos los archivos)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "chart_boxplot_variability.png", dpi=150)
    plt.close(fig)


def chart_avg_by_language_log(summary: pd.DataFrame):
    """Igual que chart_avg_by_language pero en escala log, para apreciar Rust."""
    avg_by_lang = summary.groupby("lenguaje")["tiempo_promedio_s"].mean() * 1000

    fig, ax = plt.subplots(figsize=(7, 5))
    langs = avg_by_lang.index.tolist()
    values = avg_by_lang.values
    colors = [COLORS.get(l, "#888888") for l in langs]

    bars = ax.bar(langs, values, color=colors)
    ax.set_yscale("log")
    ax.set_ylabel("Tiempo promedio (ms, escala logaritmica)")
    ax.set_title("Tiempo promedio de parseo por lenguaje (escala log)")
    ax.bar_label(bars, fmt="%.2f ms")
    ax.grid(axis="y", linestyle="--", alpha=0.4, which="both")

    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "chart_avg_by_language_log.png", dpi=150)
    plt.close(fig)


def main():
    summary = pd.read_csv(RESULTS_DIR / "benchmark_summary.csv")
    raw = pd.read_csv(RESULTS_DIR / "benchmark_raw.csv")

    chart_avg_by_language(summary)
    chart_avg_by_language_log(summary)
    chart_by_file(summary)
    chart_vs_size(summary)
    chart_boxplot(raw)

    print("Graficas generadas en:", RESULTS_DIR)
    for f in sorted(RESULTS_DIR.glob("*.png")):
        print(" -", f.name)


if __name__ == "__main__":
    main()
