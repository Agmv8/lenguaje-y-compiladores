# 🌟 Sintaxis Digital

> *“Transformando lenguaje en lógica computacional.”*

## 👥 Integrantes

- **Samuel Cortez** – C.I: 27.158.842 – Sección 2  
- **Alondra Moreno** – C.I: 30.331.870 – Sección 2  
- **Arnaldo Perdomo** – C.I: 30.791.551 – Sección 2  
- **Alejandro Duarte** – C.I: 28.530.657 – Sección 2  

# 📚 Tema 3: Estructuras Gramaticales y Autómatas

Este directorio contiene todas las actividades y entregas correspondientes al **Tema 3** de la asignatura *Lenguajes y Compiladores*.

---

## 🚀 Estructura de Entregables
El contenido de este tema se organiza de la siguiente manera:

* 🧠 **Simulador de la Jerarquía de Chomsky**: [`Jerarquia de chomsky.py`](./Jerarquia%20de%20chomsky.py)
  * Una aplicación visual interactiva desarrollada en Tkinter que detalla y valida cadenas para los 4 niveles de la Jerarquía de Chomsky (Tipo 0: Sin restricción, Tipo 1: Sensible al contexto, Tipo 2: Libre de contexto y Tipo 3: Regular).
* 🧹 **Higiene de Gramáticas**: [`higiene_gramaticas.py`](./higiene_gramaticas.py)
  * Scripts y demostraciones algorítmicas enfocadas en el saneamiento gramatical:
    * **Caso A**: Demostración visual de ambigüedad sintáctica mediante árboles de derivación para expresiones matemáticas.
    * **Caso B**: Algoritmo para la eliminación de recursividad izquierda.
    * **Caso C**: Algoritmo de factorización por la izquierda para resolver indeterminismo.
* ♟️ **Autómata de Ajedrez**: [`afd_ajedrez.py`](./afd_ajedrez.py)
  * Implementación y validación de un Autómata Finito Determinista (AFD) para un subconjunto de jugadas en notación PGN (Portable Game Notation).
* 🎨 **Dibujante GLC**: [`dibujante.py`](./dibujante.py)
  * Una herramienta que transforma cadenas de texto de una Gramática Libre de Contexto en formas geométricas interactivas usando Python Turtle.

---

# 📖 Manual de Usuario: Dibujante GLC 🎨

Bienvenido al **Dibujante GLC**, una herramienta sencilla que transforma letras en formas geométricas. ¡No necesitas saber programar para crear dibujos increíbles!

## 🚀 Guía Rápida de Inicio
1. **Inicia el programa**: Ejecuta el archivo `dibujante.py` desde tu terminal.
2. **Ingresa tus comandos**: Cuando aparezca el mensaje en pantalla, escribe una secuencia de letras (ejemplo: `agagagag`).
3. **¡Dibuja!**: Pulsa la tecla **Enter** y observa cómo la tortuga dibuja tu figura automáticamente.
4. **Cierra**: Cuando termines de admirar tu creación, simplemente haz clic en cualquier parte de la ventana para cerrarla.

## 🔡 Diccionario de Comandos
¿Qué quieres dibujar hoy? Combina estas letras como prefieras:

| Letra | ¿Qué hace? |
| :--- | :--- |
| **a** | **Avanza** un paso hacia adelante. |
| **g** | **Gira** 90° a la derecha. |
| **t** | **Gira** 90° a la izquierda. |
| **v** | **Gira** 120° (Ideal para triángulos). |
| **z** | **Gira** 72° (Ideal para pentágonos). |
| **y** | **Gira** 144° (Ideal para estrellas). |
| **c** | **Coloca un nodo** (un punto rojo decorativo). |

## 🌟 Inspiración: ¿Qué puedo dibujar?
Prueba estas cadenas para empezar a experimentar:

* **Un Cuadrado:** `agagagag`
* **Un Triángulo:** `avavav`
* **Una Estrella:** `ayayayayay`
* **Un Pentágono:** `azazazazaz`
* **Un camino con puntos:** `acacacac`

## 💡 Consejos para artistas
* **¡Combina!**: Puedes mezclar letras para crear figuras únicas.
* **No hay errores**: Si escribes una letra que no existe, la tortuga simplemente la ignorará. ¡No tengas miedo de experimentar!
* **¿Se detuvo?**: Si el dibujo no aparece, asegúrate de que la ventana del dibujo no esté escondida detrás de la ventana de código.

---

## 🔗 Enlace al Video Explicativo

• Enlace de Google Drive / YouTube al Video Explicativo: [AGREGAR_LINK_AQUÍ]