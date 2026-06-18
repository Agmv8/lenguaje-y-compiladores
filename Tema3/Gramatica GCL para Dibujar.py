import turtle

def dibujar_glc():
    print("--- Intérprete de Gramática GLC ---")
    print("Alfabeto disponible:")
    print("a: Avanzar | g: Girar 90° | t: Girar -90° | v: Girar 120° (Triángulo)")
    print("y: Girar 144° (Estrella) | z: Girar 72° (Pentágono) | c: Nodo rojo")
    
    # El usuario ingresa la cadena
    cadena = input("\nIntroduce tu cadena de letras: ").lower()
    
    # Configuración de la pantalla
    ventana = turtle.Screen()
    ventana.title("Resultado GLC: " + cadena)
    
    t = turtle.Turtle()
    t.speed(3)
    
    # Procesador de símbolos
    for comando in cadena:
        if comando == 'a': t.forward(50)
        elif comando == 'g': t.right(90)
        elif comando == 't': t.left(90)
        elif comando == 'v': t.right(120)
        elif comando == 'y': t.right(144)
        elif comando == 'z': t.right(72)
        elif comando == 'c': t.dot(10, "red")
            
    print("Dibujo generado. Cierra la ventana para terminar.")
    ventana.exitonclick()

if __name__ == "__main__":
    dibujar_glc()

# Ejemplos de uso:
# Cuadrado: agagagag
# Triángulo: avavav
# Estrella: ayayayayay
# Pentágono: azazazazaz
# Arbol: acacac
# nodo rojo: c
