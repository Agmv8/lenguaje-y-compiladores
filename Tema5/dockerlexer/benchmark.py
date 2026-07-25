"""
Script de benchmarking para las 3 implementaciones del Lexer-Parser de Dockerfile.

Version multiplataforma (Windows / Linux / Mac): detecta el sistema operativo
para usar el interprete de Python correcto y el nombre de ejecutable de Rust
correcto (con o sin .exe).

Mide el tiempo de ejecucion de cada version (Python, Java, Rust) sobre cada
archivo de prueba, repitiendo N veces por combinacion para reducir ruido,
y guarda los resultados en un CSV.

Uso:
    python benchmark.py       (Windows)
    python3 benchmark.py      (Linux / Mac)
"""

import subprocess
import time
import csv
import sys
import platform
import statistics
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TESTS_DIR = BASE_DIR / "tests"
RESULTS_DIR = BASE_DIR / "results"
REPETITIONS = 20  # corridas por combinacion (lenguaje, archivo)

RESULTS_DIR.mkdir(exist_ok=True)

IS_WINDOWS = platform.system() == "Windows"

# En Windows el interprete se invoca como "python"; en Linux/Mac como "python3".
PYTHON_CMD = "python" if IS_WINDOWS else "python3"

# En Windows el binario compilado de Rust necesita la extension .exe.
RUST_BINARY = "dockerlexer_rust.exe" if IS_WINDOWS else "dockerlexer_rust"


def run_python(test_file: Path):
    cmd = [PYTHON_CMD, str(BASE_DIR / "python" / "parser.py"), str(test_file)]
    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    return elapsed, result.returncode == 0, result.stderr


def run_java(test_file: Path):
    cmd = ["java", "-cp", str(BASE_DIR / "java"), "dockerlexer.Main", str(test_file)]
    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    return elapsed, result.returncode == 0, result.stderr


def run_rust(test_file: Path):
    binary_path = BASE_DIR / "rust" / RUST_BINARY
    cmd = [str(binary_path), str(test_file)]
    start = time.perf_counter()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.perf_counter() - start
        return elapsed, result.returncode == 0, result.stderr
    except FileNotFoundError as e:
        return 0.0, False, str(e)


RUNNERS = {
    "Python": run_python,
    "Java": run_java,
    "Rust": run_rust,
}


def check_prerequisites():
    """Verifica que los 3 ejecutables existan antes de correr el benchmark completo,
    para fallar rapido con un mensaje claro en vez de acumular 240 fallos silenciosos."""
    problems = []

    # Python: probar version
    try:
        subprocess.run([PYTHON_CMD, "--version"], capture_output=True, check=True)
    except Exception:
        problems.append(f"No se pudo ejecutar '{PYTHON_CMD}'. Verifica que Python este en el PATH.")

    # Java: verificar que exista el .class compilado
    java_class = BASE_DIR / "java" / "dockerlexer" / "Main.class"
    if not java_class.exists():
        problems.append(
            f"No se encontro {java_class}.\n"
            f"   Compila con: javac -d java java\\dockerlexer\\*.java   (desde la carpeta dockerlexer)"
        )

    # Rust: verificar que exista el binario
    rust_bin = BASE_DIR / "rust" / RUST_BINARY
    if not rust_bin.exists():
        problems.append(
            f"No se encontro {rust_bin}.\n"
            f"   Compila con: cd rust && rustc -O src\\main.rs -o {RUST_BINARY}   (Windows)\n"
            f"   o bien:      cd rust && rustc -O src/main.rs -o {RUST_BINARY}    (Linux/Mac)"
        )

    if problems:
        print("=" * 60)
        print("ATENCION: faltan prerrequisitos antes de correr el benchmark:")
        print("=" * 60)
        for p in problems:
            print(f"- {p}\n")
        print("Corrige lo anterior y vuelve a ejecutar este script.")
        sys.exit(1)


def main():
    print(f"Sistema operativo detectado: {platform.system()}")
    check_prerequisites()

    test_files = sorted(TESTS_DIR.glob("*.dockerfile"))
    if not test_files:
        print("No se encontraron archivos de prueba en", TESTS_DIR)
        return

    print(f"Archivos de prueba encontrados: {len(test_files)}")
    print(f"Repeticiones por combinacion: {REPETITIONS}")
    print(f"Lenguajes: {', '.join(RUNNERS.keys())}")
    print("-" * 60)

    raw_rows = []       # cada corrida individual
    summary_rows = []   # promedio/desviacion por combinacion
    any_failures = False

    for test_file in test_files:
        file_size_bytes = test_file.stat().st_size
        num_lines = sum(1 for _ in open(test_file))

        for lang, runner in RUNNERS.items():
            times = []
            failures = 0
            first_error = None

            # Corrida de "calentamiento" (no se mide).
            runner(test_file)

            for _ in range(REPETITIONS):
                elapsed, ok, stderr = runner(test_file)
                if not ok:
                    failures += 1
                    if first_error is None:
                        first_error = stderr.strip().splitlines()[-1] if stderr.strip() else "sin detalle"
                    continue
                times.append(elapsed)
                raw_rows.append({
                    "archivo": test_file.name,
                    "lenguaje": lang,
                    "tiempo_segundos": f"{elapsed:.6f}",
                })

            if times:
                mean = statistics.mean(times)
                stdev = statistics.stdev(times) if len(times) > 1 else 0.0
                minimum = min(times)
                maximum = max(times)
            else:
                mean = stdev = minimum = maximum = float("nan")

            summary_rows.append({
                "archivo": test_file.name,
                "lineas": num_lines,
                "tamano_bytes": file_size_bytes,
                "lenguaje": lang,
                "tiempo_promedio_s": f"{mean:.6f}",
                "desviacion_estandar_s": f"{stdev:.6f}",
                "tiempo_min_s": f"{minimum:.6f}",
                "tiempo_max_s": f"{maximum:.6f}",
                "fallos": failures,
            })

            status = f"prom={mean*1000:7.2f} ms  desv={stdev*1000:6.2f} ms  fallos={failures}"
            print(f"{test_file.name:35s} {lang:8s} {status}")
            if failures:
                any_failures = True
                print(f"    -> primer error visto: {first_error}")

    # Guardar CSV crudo (todas las corridas individuales)
    raw_csv = RESULTS_DIR / "benchmark_raw.csv"
    with open(raw_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["archivo", "lenguaje", "tiempo_segundos"])
        writer.writeheader()
        writer.writerows(raw_rows)

    # Guardar CSV resumen (promedios por combinacion)
    summary_csv = RESULTS_DIR / "benchmark_summary.csv"
    with open(summary_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "archivo", "lineas", "tamano_bytes", "lenguaje",
            "tiempo_promedio_s", "desviacion_estandar_s",
            "tiempo_min_s", "tiempo_max_s", "fallos",
        ])
        writer.writeheader()
        writer.writerows(summary_rows)

    print("-" * 60)
    print(f"CSV crudo guardado en:    {raw_csv}")
    print(f"CSV resumen guardado en:  {summary_csv}")

    if any_failures:
        print()
        print("ATENCION: hubo fallos en al menos una combinacion (archivo, lenguaje).")
        print("Revisa los mensajes '-> primer error visto' arriba antes de usar estos resultados")
        print("para las graficas o el informe: un promedio con fallos no es representativo.")


if __name__ == "__main__":
    main()