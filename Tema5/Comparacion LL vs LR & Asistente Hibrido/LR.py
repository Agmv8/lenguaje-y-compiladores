class LRShiftReduceParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = []

    def parse(self):
        for token_type, val in self.tokens:
            # Shift
            self.stack.append((token_type, val))
            # Reduce
            self.reduce()
        
        if len(self.stack) == 1 and self.stack[0][0] == 'E':
            return self.stack[0][1]
        raise SyntaxError("Error de sintaxis en Parser LR")

    def reduce(self):
        # Reduce E + NUM -> E
        if len(self.stack) >= 3 and self.stack[-3][0] == 'E' and self.stack[-2][0] == 'PLUS' and self.stack[-1][0] == 'NUM':
            v1 = self.stack[-3][1]
            v2 = int(self.stack[-1][1])
            self.stack = self.stack[:-3]
            self.stack.append(('E', v1 + v2))
        # Reduce NUM -> E
        elif len(self.stack) >= 1 and self.stack[-1][0] == 'NUM':
            v = int(self.stack[-1][1])
            self.stack.pop()
            self.stack.append(('E', v))

# Prueba: "5 + 3"
tokens_lr = [('NUM', '5'), ('PLUS', '+'), ('NUM', '3')]
parser_lr = LRShiftReduceParser(tokens_lr)
print("Resultado LR:", parser_lr.parse()) # Salida: 8