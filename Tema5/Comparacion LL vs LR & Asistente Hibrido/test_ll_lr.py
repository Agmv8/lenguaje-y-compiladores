# --- PRUEBAS DE FUNCIONALIDAD LL(1) Y LR(1) ---

from LL import LLParser
from LR import LRShiftReduceParser

# Caso 1: Entrada básica "5 + 3"
tokens_1 = [('NUM', '5'), ('PLUS', '+'), ('NUM', '3')]

p_ll1 = LLParser(tokens_1)
p_lr1 = LRShiftReduceParser(tokens_1)

assert p_ll1.parse_E() == 8, "Error en LL(1) Caso 1"
assert p_lr1.parse() == 8, "Error en LR Caso 1"

# Caso 2: Encadenamiento "10 + 20 + 5"
tokens_2 = [('NUM', '10'), ('PLUS', '+'), ('NUM', '20'), ('PLUS', '+'), ('NUM', '5')]

p_ll2 = LLParser(tokens_2)
p_lr2 = LRShiftReduceParser(tokens_2)

assert p_ll2.parse_E() == 35, "Error en LL(1) Caso 2"
assert p_lr2.parse() == 35, "Error en LR Caso 2"

print("✅ Todos los tests para LL(1) y LR(1) pasaron exitosamente (100% funcionales).")