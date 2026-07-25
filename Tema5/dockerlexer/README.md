# dockerlexer — Lexer-Parser de Dockerfile en 3 lenguajes

Implementación funcionalmente equivalente de un **Lexer-Parser para archivos Dockerfile**, escrita tres veces (Python, Java, Rust) siguiendo exactamente la misma especificación de tokens y gramática, con el fin de comparar su rendimiento en igualdad de condiciones (Preguntas 4 y 5 del trabajo práctico).

Las tres implementaciones reciben la ruta de un `.dockerfile` por línea de comandos y devuelven, por salida estándar, el mismo AST en formato JSON.

## Estructura del repositorio

```
dockerlexer/
├── python/               # Implementación en Python 3 (interpretado)
│   ├── lexer.py
│   └── parser.py
├── java/                 # Implementación en Java 21 (JVM)
│   ├── Lexer.java
│   ├── Parser.java
│   └── Main.java
├── rust/                 # Implementación en Rust 1.75 (código nativo)
│   ├── lexer.rs
│   ├── parser.rs
│   └── main.rs
├── tests/                # 12 Dockerfiles de prueba
│   ├── test01_simple.dockerfile
│   ├── test02_minimal.dockerfile
│   ├── test03_arg_before_from.dockerfile
│   ├── test04_multiline_run.dockerfile
│   ├── test05_comments.dockerfile
│   ├── test06_multistage.dockerfile
│   ├── test07_nginx.dockerfile
│   ├── test08_java_spring.dockerfile
│   ├── test09_redis.dockerfile
│   ├── test10_large.dockerfile
│   ├── test11_postgres.dockerfile
│   └── test12_rust_chef.dockerfile
├── benchmark.py          # Mide el tiempo de las 3 implementaciones sobre los 12 archivos
├── generate_charts.py    # Genera las 5 gráficas comparativas a partir de los CSV
└── results/              # Salida de benchmark.py y generate_charts.py
    ├── benchmark_raw.csv
    ├── benchmark_summary.csv
    └── *.png
```

## 1. La especificación común

Para que la comparación de rendimiento sea válida, las tres versiones comparten **el mismo lexer conceptual y la misma gramática**, definidos antes de escribir cualquier código.

### Tokens reconocidos

| Tipo | Ejemplos |
|---|---|
| `Instruction` | `FROM`, `RUN`, `COPY`, `ADD`, `ENV`, `EXPOSE`, `WORKDIR`, `CMD`, `ENTRYPOINT`, `ARG`, `LABEL`, `USER`, `VOLUME`, `STOPSIGNAL`, `HEALTHCHECK`, `SHELL`, `MAINTAINER` |
| `Comment` | línea que empieza con `#` |
| `String` | texto entre comillas dobles |
| `Identifier` | palabras sueltas (rutas, nombres, valores) |
| `Equals` | `=` |
| `LBracket` / `RBracket` | `[` `]` |
| `Comma` | `,` |
| `Newline` / `Eof` | marcadores de control internos del lexer |

Antes de tokenizar, el lexer **resuelve las continuaciones de línea**: cualquier línea que termine en `\` se une con la siguiente en una sola "línea lógica" (ver `resolve_line_continuations` en `lexer.rs`, y su equivalente en las otras dos versiones).

### Gramática: 3 formas de argumentos

El parser reconoce, después de cada instrucción, una de estas tres formas:

1. **Forma exec** — lista entre corchetes: `CMD ["python3", "app.py"]`
2. **Forma shell** — texto plano: `WORKDIR /app`
3. **Forma key=value** — pares clave-valor: `ENV APP_ENV=production`

El parser también valida que `FROM` sea la primera instrucción relevante del archivo (se permite `ARG` antes, tal como lo especifica Docker realmente). Si aparece cualquier otra instrucción antes de `FROM`, o un token inesperado, el parser devuelve un error.

### Salida: AST en JSON

Cada nodo del AST tiene esta forma:

```json
{"instruction": "ENV", "args": ["APP_ENV", "production"], "form": "key_value"}
```

El archivo completo se imprime como una lista de estos nodos. Las tres implementaciones producen **byte a byte el mismo JSON** para el mismo Dockerfile de entrada — esto es lo que se verificó antes de correr el benchmarking, y es la garantía de que las diferencias de tiempo medidas se deben al lenguaje, no a diferencias funcionales.

## 2. Cómo está organizado el código (usando Rust como referencia)

La estructura interna es la misma en las tres versiones — solo cambia la sintaxis del lenguaje:

- **`lexer.rs` / `Lexer.java` / `lexer.py`**
  - `resolve_line_continuations`: une líneas terminadas en `\`.
  - `tokenize_line`: identifica si la línea es un comentario, una instrucción conocida (`is_instruction`) o algo inválido.
  - `tokenize_arguments`: decide entre forma exec (si el resto de la línea empieza con `[`) o forma shell/key-value (recorriendo palabra por palabra y buscando `=`).
  - `tokenize`: función pública que encadena todo lo anterior y devuelve la lista completa de tokens, terminando en un token `Eof`.

- **`parser.rs` / `Parser.java` / `parser.py`**
  - Recibe la lista de tokens y avanza sobre ella con un puntero (`pos`) usando `peek` / `advance`.
  - `parse`: bucle principal; por cada token de tipo `Instruction` arma un nodo (`parse_instruction`), valida la regla de `FROM`, e ignora comentarios y saltos de línea.
  - `parse_exec_form`: consume tokens dentro de `[ ]`, separados por comas, quedándose solo con los `String`.
  - `parse_shell_or_kv_form`: recorre identificadores; si encuentra un `=` en el medio, marca el nodo como `key_value`, si no, como `shell`.
  - `Node::to_json` / equivalente: serializa el nodo manualmente a JSON (sin librerías externas) para mantener la salida idéntica entre lenguajes.

- **`main.rs` / `Main.java` / `parser.py` (bloque `__main__`)**
  - Punto de entrada por línea de comandos: recibe la ruta del archivo, lo lee, llama al parser, e imprime el AST en JSON por `stdout`. Si hay error de lectura o de parseo, lo imprime por `stderr` y termina con código de salida distinto de cero.

## 3. Cómo compilar y ejecutar cada versión

### Python 3
```bash
python3 python/parser.py tests/test01_simple.dockerfile
```
No requiere compilación; se ejecuta directo con el intérprete.

### Java 21
```bash
javac -d java java/*.java
java -cp java dockerlexer.Main tests/test01_simple.dockerfile
```
> Nota: la versión Java se implementó **a mano**, sin generador ANTLR, porque el entorno de desarrollo no tenía acceso a Maven Central ni a antlr.org durante el desarrollo. El resultado funcional es equivalente al de una implementación generada con ANTLR.

### Rust 1.75
```bash
cd rust
rustc -O main.rs -o dockerlexer_rust
./dockerlexer_rust ../tests/test01_simple.dockerfile
```
`-O` activa las optimizaciones del compilador; es el binario que usa `benchmark.py`.

## 4. Cómo correr el benchmarking

```bash
python3 benchmark.py
```

Qué hace:
1. Recorre los 12 archivos de `tests/`.
2. Por cada combinación (archivo, lenguaje): ejecuta 1 corrida de calentamiento (no medida) + 20 repeticiones medidas, invocando el binario/intérprete correspondiente como subproceso y cronometrando con `time.perf_counter()`.
3. Guarda cada corrida individual en `results/benchmark_raw.csv` y el resumen estadístico (promedio, desviación estándar, mínimo, máximo) en `results/benchmark_summary.csv`.

Total: 12 archivos × 3 lenguajes × 20 repeticiones = **720 corridas**, sin fallos registrados.

## 5. Cómo generar las gráficas

```bash
python3 generate_charts.py
```

Lee los dos CSV de `results/` (con `pandas`) y genera, con `matplotlib`, 5 imágenes en `results/`:

| Archivo | Contenido |
|---|---|
| `chart_avg_by_language.png` | Tiempo promedio por lenguaje (escala lineal) |
| `chart_avg_by_language_log.png` | Misma comparación, escala logarítmica |
| `chart_by_file.png` | Tiempo promedio por cada uno de los 12 archivos, agrupado por lenguaje |
| `chart_time_vs_size.png` | Tiempo promedio vs. número de líneas del archivo |
| `chart_boxplot_variability.png` | Distribución (boxplot) de las 720 mediciones |

## 6. Resultado resumido

| Lenguaje | Tiempo promedio | Desviación típica | Naturaleza de la ejecución |
|---|---|---|---|
| Rust (nativo) | 1.59 ms | ± 0.20 ms | Binario nativo, sin VM ni intérprete |
| Python (interpretado) | 23.24 ms | ± 3.5 ms | Intérprete CPython, arranque por proceso |
| Java (JVM) | 57.26 ms | ± 5.0 ms | Arranque de JVM + bytecode interpretado/JIT |

**Hallazgo principal:** el tiempo de ejecución se mantiene prácticamente plano sin importar el tamaño del archivo (2 a 60+ líneas) — el costo está dominado por el arranque del proceso/runtime, no por la complejidad del parseo en sí. Esto explica por qué Java, pese a ser compilado, resulta el más lento: cada corrida arranca una JVM nueva, cuyo costo de inicialización supera ampliamente el trabajo real de tokenizar y parsear (del orden de microsegundos).

Detalle completo del análisis en `Informe_Implementacion_Preguntas_4_5.docx`.

## 7. Requisitos

- Python 3.8+ (con `pandas` y `matplotlib` instalados, solo para `benchmark.py` y `generate_charts.py`)
- JDK 21+
- Rust 1.75+ (`rustc`)
