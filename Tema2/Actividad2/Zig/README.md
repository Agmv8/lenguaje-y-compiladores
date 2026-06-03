# Benchmark — Conjetura de Collatz en Zig

**Asignación II — Lenguaje y Compiladores 2026-I | UNEG**  
**Lenguaje:** Zig | **Algoritmo:** Conjetura de Collatz

---

## ¿Qué hace este programa?

Demuestra la **Conjetura de Collatz** para todos los números enteros desde 2 hasta `LIMITE`.

La conjetura establece que, dado cualquier número entero positivo `n`:
- Si `n` es **par** → `n = n / 2`
- Si `n` es **impar** → `n = 3n + 1`
- Repite hasta llegar a `1`

El programa calcula cuántos pasos necesita cada número y al final reporta cuál tardó más, junto con el **tiempo total de ejecución** en milisegundos.

---

## Requisitos

| Herramienta | Versión mínima | Descarga |
|---|---|---|
| Zig | 0.12.0 o superior | https://ziglang.org/download/ |

Para verificar que Zig está instalado:
```bash
zig version
```

---

## Cómo compilar y ejecutar

### Opción 1 — Compilar y ejecutar en un solo paso
```bash
zig run benchmark.zig -O ReleaseFast
```

### Opción 2 — Compilar primero, ejecutar después
```bash
# Compilar (genera benchmark.exe en Windows o ./benchmark en Linux/Mac)
zig build-exe benchmark.zig -O ReleaseFast

# Ejecutar en Windows
.\benchmark.exe

# Ejecutar en Linux / Mac
./benchmark
```

> **Importante:** El flag `-O ReleaseFast` activa las optimizaciones máximas de LLVM.  
> Sin él el programa corre en modo Debug y será significativamente más lento.

---

## Configurar el tamaño del benchmark

En la línea 12 del archivo `benchmark.zig` puedes ajustar el valor de `LIMITE`:

```zig
const LIMITE: u64 = 1_000_000; // cambia este número
```

| LIMITE | Propósito |
|---|---|
| `10_000` | Prueba rápida para verificar que compila |
| `1_000_000` | Benchmark estándar del informe |
| `5_000_000` | Carga máxima para comparación con Python/JS |

---

## Salida esperada

Al ejecutar con `LIMITE = 1_000_000` verás algo similar a:

```
=== Benchmarking: Conjetura de Collatz ===
Calculando para todos los n < 1000000

Resultado:
  Numero con mas pasos: 837799
  Cantidad de pasos:    524

Tiempo de ejecucion:   411 ms
```

---

## Especificaciones del hardware de prueba

| Componente | Detalle |
|---|---|
| CPU | Intel Xeon @ 2.80 GHz |
| RAM | 3.9 GB |
| SO | Windows 11 / Linux x86_64 |
| Compilador Zig | 0.13.0 con backend LLVM |
| Flag de optimización | `-O ReleaseFast` |

---

## Estructura del repositorio

```
/
├── benchmark.zig       ← Código fuente Zig (este archivo)
├── README.md           ← Este archivo
├── /python/
│   └── benchmark.py    ← Código fuente Python
├── /javascript/
│   └── benchmark.js    ← Código fuente JavaScript
└── /rust/
    └── benchmark.rs    ← Código fuente Rust
```

---

## Resultados comparativos del benchmarking

Todos los lenguajes resuelven el mismo problema (Collatz para n < 1,000,000):

| Lenguaje | Paradigma | Mecanismo | Tiempo (ms) | Memoria (MB) |
|---|---|---|---|---|
| **Zig** | Imperativo / Estructurado | Compilación nativa LLVM | ~411 | ~2.1 |
| **Rust** | Multiparadigma | Compilación nativa LLVM | ~90 | ~2.3 |
| **JavaScript** | Multiparadigma | JIT V8 Engine | ~1,550 | ~28.0 |
| **Python** | Multiparadigma | Interpretado CPython | ~12,230 | ~18.5 |

---

## Autor

**[Tu nombre]** — Ingeniería en Informática, UNEG 2026-I  
Profesor: Félix Márquez
