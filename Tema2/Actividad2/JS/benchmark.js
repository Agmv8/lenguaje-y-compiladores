const { performance } = require('perf_hooks');

// Función que calcula la cantidad de pasos de la conjetura de Collatz para un número
function collatz(n) {
    let steps = 0;
    while (n > 1) {
        if (n % 2 === 0) {
            n = n / 2;
        } else {
            n = 3 * n + 1;
        }
        steps++;
    }
    return steps;
}

// Función principal de benchmarking
function runBenchmark(limit) {
    console.log(`Iniciando benchmark de Conjetura de Collatz para n=${limit}...`);

    // Forzar recolección de basura si se ejecuta con --expose-gc para mediciones más precisas
    if (global.gc) {
        global.gc();
    }

    const memoryBefore = process.memoryUsage();
    const startTime = performance.now();

    // Ejecutar el algoritmo
    for (let i = 1; i <= limit; i++) {
        collatz(i);
    }

    const endTime = performance.now();
    const memoryAfter = process.memoryUsage();

    const timeTaken = endTime - startTime;

    // Cálculo de memoria consumida en MB (Heap Used)
    const memoryUsed = (memoryAfter.heapUsed - memoryBefore.heapUsed) / 1024 / 1024;

    console.log(`\n--- Resultados Benchmarking JavaScript ---`);
    console.log(`Paradigma Dominante: Multiparadigma (Prototípico, Funcional)`);
    console.log(`Mecanismo de Ejecución: JIT (Just-In-Time) / V8 Engine`);
    console.log(`Tiempo de Ejecución: ${timeTaken.toFixed(2)} ms`);
    console.log(`Variación de Consumo de Memoria Heap: ${memoryUsed > 0 ? memoryUsed.toFixed(2) : Math.abs(memoryUsed).toFixed(2)} MB`);

    // Note: Node.js memory management is garbage collected, so heap variation might be negative 
    // or very small for CPU bound tasks without large object allocations.
}

// Se utiliza un N suficientemente grande (n > 50) para generar carga de procesamiento visible
const N = 5000000;
runBenchmark(N);
