# Analizador Léxico para un Subconjunto de Rust usando FLEX

Este repositorio contiene la implementación práctica de un analizador léxico (lexer) automatizado para un subconjunto estructurado del lenguaje **Rust**, desarrollado como parte del Tema 4 (Análisis Léxico) de la cátedra de Lenguaje y Compiladores[cite: 1].

## 🛠️ Tecnologías Utilizadas
* **Subsistema de Windows para Linux (WSL):** Entorno operativo Ubuntu.
* **FLEX (Fast Lexical Analyzer Generator):** Metacompilador léxico para la generación del AFD[cite: 1].
* **GCC (GNU Compiler Collection):** Compilador nativo para código C[cite: 1].

## 📁 Estructura del Proyecto

<pre>
Actividad3_Rust_Flex/
├── rust_lexer.l      # Archivo de especificación léxica de Flex
├── lex.yy.c          # Archivo fuente en C generado por Flex
├── rust_lexer        # Ejecutable binario compilado (Linux)
└── prueba.rs         # Archivo de prueba con sintaxis fuente de Rust
</pre>

---

## 🚀 Requisitos de Instalación e Implementación
Para ejecutar este analizador, abra su terminal de Ubuntu (WSL) y siga las instrucciones correspondientes:

### 1. Instalación de Dependencias
Asegúrese de contar con las herramientas de compilación instaladas ejecutando en su consola:

> **sudo apt update && sudo apt install -y flex build-essential**

### 2. Navegación al Directorio del Proyecto
Mueva la terminal hacia la ubicación de las actividades compartidas de Windows (ajuste la ruta si su usuario difiere):

> **cd "/mnt/c/Users/aleja/Documents/Universidad/Semestre 7/Lenguajes y Compiladores/Actividad3_Rust_Flex"**

### 3. Proceso de Generación y Compilación
Ejecute Flex para transformar las reglas léxicas a código fuente C[cite: 1]:

> **flex rust_lexer.l**

Compile el archivo generado por el metacompilador para obtener el binario ejecutable[cite: 1]:

> **gcc lex.yy.c -o rust_lexer**

### 4. Ejecución del Analizador Léxico
Procese el archivo de código fuente de prueba (`prueba.rs`) para generar la tokenización completa por pantalla[cite: 1]:

> **./rust_lexer prueba.rs**