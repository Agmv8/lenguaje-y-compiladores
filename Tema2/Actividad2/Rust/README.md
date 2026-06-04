# Validación de la Conjetura de Collatz en Rust 🦀

Este proyecto consiste en la implementación y evaluación de rendimiento de un algoritmo iterativo diseñado para validar la **Conjetura de Collatz** ($3n + 1$) de forma secuencial para todos los números enteros en el rango matemático $[1, 100]$.

Este desarrollo forma parte de una actividad práctica de **benchmarking** destinada a evaluar y comparar la eficiencia en el tiempo de procesamiento y el consumo de recursos de Rust frente a entornos interpretados o basados en máquinas virtuales (como Python y JavaScript) y otros lenguajes de sistemas (como Zig).

---

## 🛠️ Características del Algoritmo

El programa procesa de forma consecutiva cada número evaluando las siguientes reglas aritméticas hasta reducir la secuencia al bucle cerrado unitario ($1$):
1. **Validación Par:** Si el número actual $x$ es par, se reduce mediante la operación: $x = \frac{x}{2}$.
2. **Validación Impar:** Si el número actual $x$ es impar, se transforma mediante la operación: $x = 3x + 1$.
3. **Control del Entorno:** Todo el procesamiento matemático se ejecuta utilizando memoria estática en la pila (*stack*), evitando sobrecostos de asignación dinámica.

---

## 🚀 Instrucciones de Ejecución

Al estar desarrollado bajo el ecosistema oficial de Rust, el proyecto incluye un entorno gestionado por **Cargo**.

### Requisitos Previos
* Tener instalado el compilador de Rust y Cargo (mediante `rustup`).

### Pasos para Ejecutar:
1. Abre una terminal dentro de la carpeta raíz del proyecto (`conjetura_collatz`).
2. Compila y ejecuta la aplicación optimizada con el siguiente comando nativo:
   ```bash
   cargo run --release