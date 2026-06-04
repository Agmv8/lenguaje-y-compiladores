import time
import gc

def collatz(n: int) -> int:
    steps = 0
    while n > 1:
        if n % 2 == 0:
            n = n // 2  # División entera para mantener el tipo int
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def run_benchmark(limit: int):
    print(f"Iniciando benchmark de Conjetura de Collatz para n={limit}...")

    # Forzar recolección de basura inicial para estabilizar el entorno
    gc.collect()
    
    # Captura del tiempo inicial en nanosegundos utilizando el reloj de hardware
    start_time = time.perf_counter_ns()

    # Ejecutar el algoritmo de carga masiva
    for i in range(1, limit + 1):
        collatz(i)

    # Captura del tiempo final en nanosegundos
    end_time = time.perf_counter_ns()

    # Cálculo de la diferencia y conversión a milisegundos (ms)
    time_taken_ms = (end_time - start_time) / 1_000_000

    print("\n--- Resultados Benchmarking Python ---")
    print("Paradigma Dominante: Multiparadigma (OO, Imperativo, Funcional)")
    print("Mecanismo de Ejecución: Interpretado (CPython / Máquina Virtual)")
    print(f"Tiempo de Ejecución: {time_taken_ms:.2f} ms")
    print("Consumo de Memoria: Gestionado dinámicamente por asignación de objetos (Pila/Heap unificados)")

if __name__ == "__main__":
    N = 1000000
    run_benchmark(N)