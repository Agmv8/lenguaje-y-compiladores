import re

def procesar_jugada(jugada: str) -> bool:
    """
    Valida una jugada de ajedrez basada en el subconjunto PGN definido.
    
    Lógica de estados:
    - q0: Estado inicial.
    - q1: Se recibió una pieza (N, B, R, Q, K).
    - q2: Se recibió una columna (a-h).
    - qf: Estado de aceptación tras recibir fila (1-8).
    """
    # Expresión regular que representa las transiciones del AFD
    # [Pieza][Columna][Fila] | [Columna][Fila]
    patron = r'^([NBRQK][a-h][1-8]|[a-h][1-8])$'
    
    return bool(re.match(patron, jugada))

# Pruebas del AFD
if __name__ == "__main__":
    pruebas = ["e4", "Nf3", "Ra8", "z9", "N1", "e9"]
    for p in pruebas:
        resultado = "Aceptada" if procesar_jugada(p) else "Rechazada"
        print(f"Jugada: {p} -> {resultado}")