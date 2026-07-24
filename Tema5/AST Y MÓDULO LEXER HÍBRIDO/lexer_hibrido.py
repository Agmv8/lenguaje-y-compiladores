import re
import difflib

# 1. Palabras clave del lenguaje
KEYWORDS = {'if', 'else', 'while', 'print', 'return', 'int', 'float'}

# 2. Reglas léxicas corregidas y ordenadas
TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),       # Números
    ('STRING',   r'"[^"]*"'),           # Cadenas de texto como "no"
    ('KEYWORD',  r'[a-zA-Z_]\w*'),      # Palabras (evaluaremos si es KW, ID o error)
    ('ASSIGN',   r'='),                 # =
    ('OP',       r'[+\-*/><]'),         # Operadores
    ('LPAREN',   r'\('),                # (
    ('RPAREN',   r'\)'),                # )
    ('SEMI',     r';'),                 # ;
    ('SKIP',     r'[ \t\n]+'),          # Espacios
    ('MISMATCH', r'.'),                 # Caracteres extraños
]

def mock_llm_fallback(token_ambiguo):
    prompt = f"Corrige este token ambiguo en contexto de UnegScript: '{token_ambiguo}'"
    diccionario_ia = {'prnt': 'print', 'pront': 'print', 'fi': 'if'}
    sugerencia = diccionario_ia.get(token_ambiguo, token_ambiguo)
    return sugerencia, f"IA Prompt: '{prompt}' -> Resuelto a '{sugerencia}'"

def lexer_hibrido(code):
    tokens = []
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPEC)
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        
        if kind == 'SKIP':
            continue
        elif kind == 'KEYWORD':
            # Si es palabra clave exacta (ej: if)
            if value in KEYWORDS:
                tokens.append(('TK_' + value.upper(), value))
            else:
                # Comprobar si fue un intento fallido de palabra clave
                best_match = None
                best_ratio = 0.0
                
                for kw in KEYWORDS:
                    ratio = difflib.SequenceMatcher(None, value, kw).ratio()
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_match = kw
                
                # Si se parece bastante a una Keyword (0.5 <= ratio < 1.0)
                if best_ratio >= 0.8:
                    print(f"[Lexer Auto-Fix] '{value}' -> '{best_match}' (Confianza difflib: {best_ratio:.2f})")
                    tokens.append(('TK_' + best_match.upper(), best_match))
                elif best_ratio >= 0.5:
                    sugerencia, log_ia = mock_llm_fallback(value)
                    print(f"[Lexer Fallback IA] '{value}' (Confianza difflib baja: {best_ratio:.2f})")
                    print(f" -> {log_ia}")
                    tokens.append(('TK_' + sugerencia.upper(), sugerencia))
                else:
                    # Si no se parece a ninguna palabra clave (ej: variable 'x'), es un ID normal
                    tokens.append(('TK_ID', value))
                    
        elif kind == 'STRING':
            tokens.append(('TK_STRING', value))
        elif kind == 'MISMATCH':
            print(f"[Error Léxico] Carácter no reconocido: {value}")
        else:
            tokens.append((f'TK_{kind}', value))
            
    return tokens

if __name__ == "__main__":
    codigo_prueba = 'pront x=5; if x>3 prnt(x) else prnt("no")'
    print("--- INICIANDO ANÁLISIS LÉXICO HÍBRIDO ---")
    tokens_obtenidos = lexer_hibrido(codigo_prueba)

    print("\n--- TOKENS GENERADOS ---")
    print(tokens_obtenidos)