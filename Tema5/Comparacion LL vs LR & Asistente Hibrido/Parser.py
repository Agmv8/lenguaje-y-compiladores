import re
from difflib import SequenceMatcher

# ==========================================
# 1. LEXER HÍBRIDO + DISTANCIA LEVENSHTEIN
# ==========================================
KEYWORDS = {"if", "else", "print"}

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def ai_suggest_keyword(token_str):
    """Simula o consulta IA / Levenshtein para autoconregir tokens léxicos."""
    best_match = None
    best_score = 0.0
    for kw in KEYWORDS:
        score = similarity(token_str, kw)
        if score > best_score:
            best_score = score
            best_match = kw
    
    if best_score >= 0.5:
        return best_match, best_score
    return token_str, 0.0

def lexer_unegscript(code):
    # Definición de tokens mediante regex
    raw_tokens = re.findall(r'[a-zA-Z_]\w*|\d+|==|<=|>=|>|<|=|\(|\)|;|"[^"]*"|\S', code)
    
    corrected_tokens = []
    suggestions = []
    
    for t in raw_tokens:
        if re.match(r'^[a-zA-Z_]\w*$', t):
            if t in KEYWORDS:
                corrected_tokens.append(('KEYWORD', t))
            else:
                # Intento de corrección si es un error tipográfico tipo 'pront' o 'prnt'
                match, score = ai_suggest_keyword(t)
                if score >= 0.6 and match != t:
                    suggestions.append(f"Sugerencia Léxica (IA): '{t}' -> '{match}' (confianza: {score:.2f})")
                    corrected_tokens.append(('KEYWORD', match))
                else:
                    corrected_tokens.append(('ID', t))
        elif re.match(r'^\d+$', t):
            corrected_tokens.append(('INT', int(t)))
        elif t in {'=', '>', '<', '>=', '<=', '=='}:
            corrected_tokens.append(('OP', t))
        elif t in {'(', ')', ';', '{', '}'}:
            corrected_tokens.append(('PUNCT', t))
        elif t.startswith('"') and t.endswith('"'):
            corrected_tokens.append(('STRING', t[1:-1]))
        else:
            corrected_tokens.append(('UNKNOWN', t))
            
    return corrected_tokens, suggestions

# ==========================================
# 2. PARSER RECURSIVO DESCENDENTE CON LOOKAHEAD
# ==========================================
class UnegScriptParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def lookahead(self):
        """Retorna el token actual sin consumirlo (Lookahead = 1)."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', 'EOF')

    def consume(self, expected_val=None):
        tok = self.lookahead()
        if expected_val and tok[1] != expected_val:
            raise SyntaxError(f"Se esperaba '{expected_val}', pero se encontró '{tok[1]}'")
        self.pos += 1
        return tok

    def parse_program(self):
        statements = []
        while self.lookahead()[0] != 'EOF':
            statements.append(self.parse_statement())
        return {"Type": "Program", "Body": statements}

    def parse_statement(self):
        tok_type, tok_val = self.lookahead()
        
        # Sentencia IF
        if tok_val == 'if':
            self.consume('if')
            condition = self.parse_expression()
            
            # Verificación/Recuperación suave de sintaxis para paréntesis opcionales u omisión
            body = self.parse_statement()
            
            else_body = None
            if self.lookahead()[1] == 'else':
                self.consume('else')
                else_body = self.parse_statement()
                
            return {
                "Type": "IfStatement",
                "Condition": condition,
                "Then": body,
                "Else": else_body
            }
        
        # Sentencia PRINT
        elif tok_val == 'print':
            self.consume('print')
            has_paren = False
            if self.lookahead()[1] == '(':
                self.consume('(')
                has_paren = True
            
            arg = self.parse_expression()
            
            if has_paren:
                self.consume(')')
                
            # Opcional consumición de ';'
            if self.lookahead()[1] == ';':
                self.consume(';')
                
            return {"Type": "PrintStatement", "Argument": arg}
        
        # Asignación
        elif tok_type == 'ID':
            var_name = self.consume()[1]
            self.consume('=')
            expr = self.parse_expression()
            if self.lookahead()[1] == ';':
                self.consume(';')
            return {"Type": "Assignment", "Variable": var_name, "Value": expr}
            
        else:
            raise SyntaxError(f"Estructura sintáctica no reconocida cerca de '{tok_val}'")

    def parse_expression(self):
        left_type, left_val = self.consume()
        
        # Expresión binaria (ej. x > 3)
        if self.lookahead()[0] == 'OP':
            op = self.consume()[1]
            right = self.parse_expression()
            return {
                "Type": "BinaryExpression",
                "Left": left_val,
                "Operator": op,
                "Right": right
            }
            
        return {"Type": "Literal", "Value": left_val}

# ==========================================
# 3. EJECUCIÓN Y SALIDA FORMATEADA
# ==========================================
code_input = 'pront x=5; if x>3 prnt(x) else prnt("no")'

# Paso 1: Lexer y corrección
corrected_tokens, suggestions = lexer_unegscript(code_input)

# Sugerencias semánticas/sintácticas adicionales por IA
if any(t[1] == 'if' for t in corrected_tokens):
    if not any(t[1] == '(' for t in corrected_tokens):
        suggestions.append("Sugerencia Sintáctica (IA): Se recomienda envolver la condición del 'if' entre paréntesis '(' ')' para mejorar la legibilidad.")

# Paso 2: Parsing para construir AST
parser = UnegScriptParser(corrected_tokens)
ast = parser.parse_program()

# Imprimir Resultados Formateados
print("==================================================")
print("1. TOKENS CORREGIDOS:")
print("==================================================")
print(corrected_tokens)

print("\n==================================================")
print("2. SUGERENCIAS BRINDADAS POR LA IA:")
print("==================================================")
for sug in suggestions:
    print(f"- {sug}")

print("\n==================================================")
print("3. AST GENERADO:")
print("==================================================")
import json
print(json.dumps(ast, indent=2))