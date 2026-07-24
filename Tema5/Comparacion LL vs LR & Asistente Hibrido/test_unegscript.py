from Parser import UnegScriptParser, lexer_unegscript


def probar_caso(nombre_caso, codigo_fuente):
    print(f"\n==================================================")
    print(f"EJECUTANDO: {nombre_caso}")
    print(f"Entrada: {codigo_fuente}")
    print(f"==================================================")
    
    # 1. Análisis Léxico + Corrección IA
    tokens, sugerencias = lexer_unegscript(codigo_fuente)
    
    print("Tokens Obtenidos/Corregidos:")
    print(tokens)
    
    print("\nSugerencias de la IA:")
    if sugerencias:
        for s in sugerencias:
            print(f" - {s}")
    else:
        print(" - Ninguna (Código limpio)")

    # 2. Análisis Sintáctico (AST)
    try:
        parser = UnegScriptParser(tokens)
        ast = parser.parse_program()
        print("\nAST Generado Correctamente:")
        import json
        print(json.dumps(ast, indent=2))
        print("\nRESULTADO: ✅ ÉXITO")
    except Exception as e:
        print(f"\nRESULTADO: ❌ ERROR SINTÁCTICO -> {e}")

# --- SUITE DE PRUEBAS ---

# 1. Caso Requerido por el Profesor (con typo 'pront' y 'prnt')
probar_caso(
    "Caso Enunciado (Errores de tipeo)",
    'pront x=5; if x>3 prnt(x) else prnt("no")'
)

# 2. Caso Válido/Limpio (Sin errores)
probar_caso(
    "Caso Código Sintácticamente Limpio",
    'x = 10; if x > 5 print("mayor") else print("menor")'
)

# 3. Caso Sintaxis con Paréntesis y Múltiples Asignaciones
probar_caso(
    "Caso Anidado y con Paréntesis",
    'pront y = 100; print(y)'
)