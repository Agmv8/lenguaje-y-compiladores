# Simulación de Blockchain en Rust 🦀

Este proyecto consiste en la implementación y evaluación de rendimiento de un algoritmo de simulación de cadena de bloques (Blockchain) desarrollado en el lenguaje de programación **Rust**. La aplicación genera bloques secuenciales asegurando la integridad de los datos mediante el enlace criptográfico de hashes repetitivos.

Este desarrollo forma parte de una actividad de **benchmarking** para comparar el paradigma, mecanismo de ejecución, tiempo de procesamiento y consumo de memoria de Rust frente a otros lenguajes como Python, Zig y JavaScript.

---

## 🛠️ Características del Algoritmo

El programa simula el comportamiento esencial de una red blockchain mediante los siguientes componentes:
1. **Tabla de Mensajes Estáticos:** Una entrada fija de datos simulando transacciones e información del sistema.
2. **Estructura de Bloque (`struct Bloque`):** Cada bloque contiene un identificador (`id`), un cuerpo de datos (`mensaje`), el hash del bloque inmediatamente anterior (`hash_anterior`) y su propio hash (`hash_actual`).
3. **Encadenamiento Criptográfico:** El `hash_actual` se calcula combinando de forma estricta el hash del bloque previo junto al mensaje en curso (`hash + mensaje`), garantizando la inmutabilidad de la estructura.
4. **Validación de Integridad:** Un bucle automatizado verifica secuencialmente que ningún eslabón de la cadena haya sido alterado.

---

## 🚀 Instrucciones de Ejecución

Al estar desarrollado bajo el ecosistema oficial de Rust, el proyecto incluye un entorno gestionado por **Cargo**.

### Requisitos Previos
* Tener instalado el compilador de Rust y Cargo (mediante `rustup`).

### Pasos para Ejecutar:
1. Abre una terminal dentro de la carpeta raíz del proyecto (`simulacion_blockchain`).
2. Compila y ejecuta la aplicación con el siguiente comando nativo:
   ```bash
   cargo run