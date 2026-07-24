import json
# 1. Importamos los módulos que ya creaste en la carpeta Tema 5
from LL import LLParser
from LR import LRShiftReduceParser
from Parser import UnegScriptParser, lexer_unegscript


def probar_teoria_ll_vs_lr():
    print("==================================================")
    print("  PARTE TEÓRICA / INFORME 1: PRUEBAS LL vs LR")
    print("==================================================")
    
    # Caso 1: Expresión "5 + 3"
    tokens_1 = [('NUM', '5'), ('PLUS', '+'), ('NUM', '3')]
    p_ll1 = LLParser(tokens_1)
    p_lr1 = LRShiftReduceParser(tokens_1)
    
    res_ll1 = p_ll1.parse_E()
    res_lr1 = p_lr1.parse()
    print(f"[TEST 1] Expresión '5 + 3' -> LL(1): {res_ll1} | LR(1): {res_lr1}")
    assert res_ll1 == 8 and res_lr1 == 8, "Error en Test 1"

    # Caso 2: Expresión "10 + 20 + 5"
    tokens_2 = [('NUM', '10'), ('PLUS', '+'), ('NUM', '20'), ('PLUS', '+'), ('NUM', '5')]
    p_ll2 = LLParser(tokens_2)
    p_lr2 = LRShiftReduceParser(tokens_2)
    
    res_ll2 = p_ll2.parse_E()
    res_lr2 = p_lr2.parse()
    print(f"[TEST 2] Expresión '10 + 20 + 5' -> LL(1): {res_ll2} | LR(1): {res_lr2}")
    assert res_ll2 == 35 and res_lr2 == 35, "Error en Test 2"

    print("\n✅ Módulo LL vs LR: 100% Funcional.\n")


def probar_caso_unegscript(nombre_caso, codigo_fuente):
    print("--------------------------------------------------")
    print(f"EJECUTANDO: {nombre_caso}")
    print(f"Entrada: {codigo_fuente}")
    print("--------------------------------------------------")
    
    # 1. Lexer + Sugerencias IA
    tokens, sugerencias = lexer_unegscript(codigo_fuente)
    
    # Sugerencia sintáctica si falta paréntesis en 'if'
    if any(t[1] == 'if' for t in tokens) and not any(t[1] == '(' for t in tokens):
        sugerencias.append("Sugerencia Sintáctica (IA): Se recomienda envolver la condición del 'if' entre paréntesis '(' ')' para mejorar la legibilidad.")

    print("\n1. TOKENS CORREGIDOS:")
    print(tokens)
    
    print("\n2. SUGERENCIAS BRINDADAS POR LA IA:")
    if sugerencias:
        for s in sugerencias:
            print(f" - {s}")
    else:
        print(" - Ninguna (Código limpio)")

    # 2. Parser -> AST
    try:
        parser = UnegScriptParser(tokens)
        ast = parser.parse_program()
        print("\n3. AST GENERADO:")
        print(json.dumps(ast, indent=2))
        print("\nRESULTADO: ✅ ÉXITO DE COMPILACIÓN\n")
    except Exception as e:
        print(f"\nRESULTADO: ❌ ERROR SINTÁCTICO -> {e}\n")


def main():
    # A) Ejecución de la teoría (LL vs LR)
    probar_teoria_ll_vs_lr()

    # B) Ejecución de la práctica (Parser UnegScript + IA)
    print("==================================================")
    print("  PARTE PRÁCTICA / CÓDIGO (PREGUNTA 5): UNEGSCRIPT")
    print("==================================================")
    
    # Caso Requerido por el Profesor (Pregunta 5)
    probar_caso_unegscript(
        "Caso Enunciado (Errores de tipeo)",
        'pront x=5; if x>3 prnt(x) else prnt("no")'
    )

    # Caso Limpio Adicional
    probar_caso_unegscript(
        "Caso Código Sin Errores",
        'x = 10; if x > 5 print("mayor") else print("menor")'
    )


if __name__ == "__main__":
    main()