# Tema 5: Análisis Sintáctico, Comparación LL vs LR y Asistente Híbrido UnegScript

Este repositorio contiene la solución completa a la actividad práctica y teórica del Tema 5 (Análisis Sintáctico) de la asignatura Lenguajes y Compiladores de la Universidad Nacional Experimental de Guayana (UNEG).

El proyecto aborda la evaluación comparativa entre algoritmos de parseo deterministas (LL y LR) y la implementación de un Parser Recursivo Descendente Híbrido en Python que integra técnicas tradicionales de compiladores con un mecanismo de Fallback a IA para la corrección automática y generación de sugerencias.

## Requerimientos del Sistema

* Sistema Operativo: Windows 10/11, macOS o Linux.
* Lenguaje de Programación: Python 3.8 o superior (probado en Python 3.13).
* Librerías / Módulos (Biblioteca estándar de Python):
  * re (Expresiones regulares para tokenización).
  * json (Visualización del AST).
  * difflib.SequenceMatcher (Cálculo del umbral de confianza)

## Estructura del Proyecto

* LL.py: Implementación del Parser LL(1) Recursivo Descendente.
* LR.py: Implementación del Parser LR(1) Shift-Reduce
* Parser.py: Lexer Híbrido + Parser UnegScript + Módulo IA
* test_ll_lr.py: Pruebas unitarias directas para el módulo LL y LR.
* test_unegscript.py: Suite de pruebas para el parser de UnegScript y Fallback IA.
* main.py: Script principal de ejecución unificada.

## Pasos para Ejecutar y Probar el Código

1. Ubicarte en la carpeta del proyecto:
   cd "Tema 5"

2. Ejecutar la Suite de Pruebas Unificada (main.py):
   * En Windows (PowerShell / Terminal):
     py main.py
   * En Linux / macOS:
     python3 main.py

## Salida Esperada en Consola

Al ejecutar main.py, la terminal mostrará:
1. Módulo Teórico LL vs LR: Evaluación y verificación determinista.
2. Tokens Corregidos: Transformación automática de "pront" y "prnt" a "print".
3. Sugerencias Emitidas por la IA y AST generado en JSON
