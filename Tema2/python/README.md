# Benchmark de la Conjetura de Collatz en Python

Este script implementa el cálculo masivo de la **Conjetura de Collatz** (también conocida como problema 3n+1) con el fin de medir el rendimiento del lenguaje Python en un escenario de procesamiento intensivo (carga de CPU).  
Los resultados obtenidos forman parte de la **Actividad II** del proyecto "Lenguajes de programación – Tema 2", donde se compara el rendimiento de Python con otros lenguajes (Zig, Rust, JavaScript).

---

##  Entorno Tecnológico y Requisitos

Para reproducir este escenario de pruebas empíricas bajo condiciones controladas, asegúrese de cumplir con los siguientes prerrequisitos:

* **Lenguaje / Intérprete:** Python 3.8 o superior (recomendado 3.11+).  
* **Entorno de Ejecución:** CPython (Máquina Virtual estándar).  
* **Módulos requeridos:** Solo se utilizan módulos de la biblioteca estándar (`time`, `gc`).  
* **Herramientas del sistema:** Terminal de comandos (Bash, PowerShell, CMD).

---

##  Instrucciones de Configuración e Instalación

Este script ha sido diseñado utilizando exclusivamente las **APIs nativas de Python** (`time.perf_counter_ns()` y `gc.collect()`), por lo que **no requiere la instalación de dependencias de terceros** (`pip install`), garantizando un aislamiento limpio del hardware.

1. Clone el repositorio o navegue hasta el directorio que contiene el script:
   ```bash
   cd ./lenguaje-y-compiladores/Tema2/python
   ```

2. Verifique que Python esté instalado correctamente:
   ```bash
   python --version
   ```

3. (Opcional) Cree un entorno virtual para aislar la prueba:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

4. Ejecute el benchmark:
   ```bash
   python benchmark.py
   ```
## Personalización del límite de ejecución:
```bash
if __name__ == "__main__":
    N = 10_000_000   # por ejemplo, 10 millones
    run_benchmark(N) 
```
