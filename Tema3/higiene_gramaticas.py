import os

def demostrar_ambiguedad_caso_a():
    """
    Simulación teórica y demostración para el Caso A.
    Muestra cómo una misma cadena genera dos interpretaciones sintácticas distintas.
    """
    print("\n--- CASO A: Demostración de Ambigüedad ---")
    print("Gramática Patológica: E -> E + E | E * E | id")
    print("Cadena a evaluar: id + id * id")
    
    # Representación en texto de las dos derivaciones posibles
    derivacion_1 = "E -> E + E -> id + E -> id + E * E -> id + id * id"
    derivacion_2 = "E -> E * E -> E + E * E -> id + E * E -> id + id * id"
    
    print(#ff0000
        f"\n[Árbol 1 - Prioriza Multiplicación (Correcto Semánticamente)]:\n"
        f"    E\n"
        f"   /|\\\n"
        f"  E + E\n"
        f"  |  /|\\\n"
        f" id E * E\n"
        f"    |   |\n"
        f"   id  id\n"
        f"Sintaxis interpretada: (id + (id * id))"
    )
    
    print(
        f"\n[Árbol 2 - Prioriza Suma (Erróneo/Ambiguo)]:\n"
        f"      E\n"
        f"     /|\\\n"
        f"    E * E\n"
        f"   /|\\  |\n"
        f"  E + E id\n"
        f"  |   |\n"
        f" id  id\n"
        f"Sintaxis interpretada: ((id + id) * id)"
    )
    print("\nResultado: Al existir dos estructuras arbóreas válidas, se comprueba la ambigüedad.")


def eliminar_recursividad_izquierda_caso_b(gramatica: dict) -> dict:
    """
    Caso B: Algoritmo matemático para eliminar la recursividad por la izquierda.
    """
    gramatica_optimizada = {}
    for no_terminal, producciones in gramatica.items():
        recursivas = []
        no_recursivas = []
        
        for prod in producciones:
            if prod.startswith(no_terminal):
                recursivas.append(prod[len(no_terminal):].strip())
            else:
                no_recursivas.append(prod)
        
        if recursivas:
            nuevo_no_terminal = f"{no_terminal}'"
            gramatica_optimizada[no_terminal] = [f"{beta} {nuevo_no_terminal}".strip() for beta in no_recursivas]
            gramatica_optimizada[nuevo_no_terminal] = [f"{alpha} {nuevo_no_terminal}".strip() for alpha in recursivas] + ["ε"]
        else:
            gramatica_optimizada[no_terminal] = producciones
            
    return gramatica_optimizada


def factorizar_por_izquierda_caso_c(no_terminal: str, producciones: list) -> dict:
    """
    Caso C: Algoritmo de factorización por la izquierda para eliminar indeterminismo.
    """
    if len(producciones) < 2:
        return {no_terminal: producciones}
    
    prods_divididas = [p.split() for p in producciones]
    prefijo_comun = []
    
    for palabras in zip(*prods_divididas):
        if len(set(palabras)) == 1:
            prefijo_comun.append(palabras[0])
        else:
            break
            
    if not prefijo_comun:
        return {no_terminal: producciones}
        
    str_prefijo = " ".join(prefijo_comun)
    nuevo_no_terminal = f"{no_terminal}'"
    
    remanentes = []
    for prod in producciones:
        remanente = prod[len(str_prefijo):].strip()
        remanentes.append(remanente if remanente != "" else "ε")
            
    return {
        no_terminal: [f"{str_prefijo} {nuevo_no_terminal}"],
        nuevo_no_terminal: remanentes
    }


def mostrar_gramatica(titulo: str, gramatica: dict):
    print(f"\n--- {titulo} ---")
    for no_terminal, producciones in gramatica.items():
        print(f"  {no_terminal} -> {' | '.join(producciones)}")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    print("=======================================================")
    print("=== REPOSITORIO DE COMPILADORES: HIGIENE GRAMATICAL ===")
    print("=======================================================")
    
    # 1. CASO A
    demostrar_ambiguedad_caso_a()
    print("\n" + "="*55)
    
    # 2. CASO B
    gramatica_recursiva = {"E": ["E + T", "T"]}
    mostrar_gramatica("CASO B: Gramática Original (Recursiva por la Izquierda)", gramatica_recursiva)
    
    gramatica_sin_recursividad = eliminar_recursividad_izquierda_caso_b(gramatica_recursiva)
    mostrar_gramatica("CASO B: Gramática Otimizada (Recursión Eliminada)", gramatica_sin_recursividad)
    print("\n" + "="*55)
    
    # 3. CASO C
    no_terminal_c = "S"
    producciones_c = ["if C then S else S", "if C then S"]
    mostrar_gramatica("CASO C: Gramática Original (Indeterminista / Requiere Factorização)", {no_terminal_c: producciones_c})
    
    gramatica_factorizada = factorizar_por_izquierda_caso_c(no_terminal_c, producciones_c)
    mostrar_gramatica("CASO C: Gramática Optimizada (Factorizada Exitosamente)", gramatica_factorizada)
    print("\n=======================================================")