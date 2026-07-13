# Actividad 2: Analizador Léxico para Dockerfile con Regex

Este directorio contiene la solución para el analizador léxico (lexer) de archivos `Dockerfile` utilizando expresiones regulares en Python.

---

## Estructura del Directorio

```text
├── Actividad2_Docker/
│   ├── docker_lexer.py          # Código fuente en Python del analizador léxico.
│   ├── docker_lexer.exe         # Ejecutable compilado para Windows de forma directa.
│   ├── Dockerfile_ejemplo1      # Ejemplo de Dockerfile válido para pruebas.
│   ├── Dockerfile_ejemplo2      # Ejemplo de Dockerfile con errores léxicos.
│   ├── Dockerfile_ejemplo3      # Ejemplo de Dockerfile con comentarios y sangrías.
│   ├── informe_actividad2.md    # Informe técnico detallado de la actividad.
│   └── README.md                # Este archivo de instrucciones.
```

---

## Cómo Ejecutar el Lexer

### Opción 1: Ejecutar el Código Fuente (Python)
Para ejecutar el script usando Python (analiza los tres Dockerfiles de prueba por defecto):
```bash
python docker_lexer.py
```
O bien, analizando un archivo personalizado:
```bash
python docker_lexer.py ruta/a/tu/Dockerfile
```

### Opción 2: Ejecutar el Binario Ejecutable
Si no dispones de Python instalado, puedes ejecutar el binario precompilado para Windows:
```cmd
.\docker_lexer.exe
```
O analizando un archivo personalizado:
```cmd
.\docker_lexer.exe ruta/a/tu/Dockerfile
```