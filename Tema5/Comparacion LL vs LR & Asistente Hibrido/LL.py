class LLParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, expected_type):
        if self.peek() and self.peek()[0] == expected_type:
            val = self.tokens[self.pos][1]
            self.pos += 1
            return val
        raise SyntaxError(f"Se esperaba {expected_type} en posición {self.pos}")

    def parse_E(self):
        num = self.match('NUM')
        return self.parse_E_prime(int(num))

    def parse_E_prime(self, left_value):
        if self.peek() and self.peek()[0] == 'PLUS':
            self.match('PLUS')
            num = self.match('NUM')
            return self.parse_E_prime(left_value + int(num))
        return left_value # Regla épsilon

# Prueba: "5 + 3"
tokens_ll = [('NUM', '5'), ('PLUS', '+'), ('NUM', '3')]
parser_ll = LLParser(tokens_ll)
print("Resultado LL(1):", parser_ll.parse_E()) # Salida: 8