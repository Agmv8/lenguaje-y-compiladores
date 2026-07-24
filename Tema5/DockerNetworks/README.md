# Docker Networks Parser

Este subdirectorio contiene la solución del proyecto: un analizador léxico‑sintáctico para la sección `networks` del archivo `docker‑compose.yml`.

## Contenido

- **`docker_networks_parser.py`** – Implementación completa con:
  - `DockerNetworksLexer` (manejo de identación, tokens `INDENT`/`DEDENT`).
  - `DockerNetworksParser` (descenso recursivo con recuperación de errores tipo *panic mode*).
  - Clases de nodos AST (`NetworksSectionNode`, `NetworkDefinitionNode`, `PropertyNode`, …).

- **`run_tests.py`** – Ejecuta el parser contra el conjunto de pruebas y muestra:
  - Tokens generados.
  - Árbol AST.
  - Mensajes de error y recuperación.

- **`test_files/`** – Casos de prueba:
  - `docker-compose-valid1.yml` – Configuración básica válida.
  - `docker-compose-valid2.yml` – Configuración avanzada con bloques `IPAM` y subredes.
  - `docker-compose-invalid-lexical.yml` – Error léxico (carácter no reconocido).
  - `docker-compose-invalid-syntax.yml` – Error sintáctico que demuestra la recuperación del parser.

## Requisitos

- Python 3.x (tested on 3.13).
- **Sin dependencias externas** – todo el código usa la biblioteca estándar.

## Uso rápido

Ejecuta todas las pruebas:

```powershell
python run_tests.py
```

Ejecuta el parser sobre un archivo concreto:

```powershell
python docker_networks_parser.py test_files/docker-compose-valid1.yml
```

## Salida esperada

- Listado de tokens con posición de línea/columna.
- Representación del AST en formato árbol.
- En caso de error, mensaje indicando la ubicación y el token de recuperación, seguido de la continuación del análisis.

---

Mantén esta estructura al agregar nuevos casos de prueba o al extender la gramática.
