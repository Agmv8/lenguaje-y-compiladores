"""
Parser para Dockerfile.
Consume la lista de tokens producida por lexer.py y construye un AST
en forma de lista de nodos (dicts), siguiendo la gramática:

dockerfile       ::= { line }
line             ::= comment | instruction_line
instruction_line ::= INSTRUCTION arguments NEWLINE
arguments        ::= exec_form | shell_form | key_value_list
exec_form        ::= LBRACKET STRING { COMMA STRING } RBRACKET
shell_form       ::= { IDENTIFIER | STRING }
key_value_list   ::= key_value { key_value }
key_value        ::= IDENTIFIER EQUALS ( IDENTIFIER | STRING )
"""

from lexer import tokenize


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        ast = []
        seen_from = False

        while self.peek().type != "EOF":
            tok = self.peek()

            if tok.type == "COMMENT":
                self.advance()
                self.expect_optional_newline()
                continue

            if tok.type == "UNKNOWN":
                raise ParseError(
                    f"Instruccion desconocida '{tok.value}' en linea {tok.line}"
                )

            if tok.type == "INSTRUCTION":
                node = self.parse_instruction()
                if node["instruction"] == "FROM":
                    seen_from = True
                elif not seen_from and node["instruction"] != "ARG":
                    raise ParseError(
                        f"La instruccion '{node['instruction']}' aparece antes de FROM "
                        f"(linea {tok.line})"
                    )
                ast.append(node)
                continue

            if tok.type == "NEWLINE":
                self.advance()
                continue

            raise ParseError(f"Token inesperado {tok.type} en linea {tok.line}")

        return ast

    def expect_optional_newline(self):
        if self.peek().type == "NEWLINE":
            self.advance()

    def parse_instruction(self):
        instr_tok = self.advance()
        instruction = instr_tok.value

        if self.peek().type == "LBRACKET":
            args, form = self.parse_exec_form()
        else:
            args, form = self.parse_shell_or_kv_form()

        self.expect_optional_newline()

        node = {"instruction": instruction, "args": args}
        if form:
            node["form"] = form
        return node

    def parse_exec_form(self):
        self.advance()  # consume '['
        args = []
        while self.peek().type != "RBRACKET":
            tok = self.peek()
            if tok.type == "STRING":
                args.append(tok.value)
                self.advance()
            elif tok.type == "COMMA":
                self.advance()
            elif tok.type == "NEWLINE":
                self.advance()
            else:
                raise ParseError(
                    f"Token inesperado {tok.type} dentro de forma exec, linea {tok.line}"
                )
        self.advance()  # consume ']'
        return args, "exec"

    def parse_shell_or_kv_form(self):
        args = []
        is_kv = False

        while self.peek().type in ("IDENTIFIER", "EQUALS", "STRING"):
            tok = self.advance()
            if tok.type == "EQUALS":
                is_kv = True
                continue
            args.append(tok.value)

        return args, ("key_value" if is_kv else "shell")


def parse_dockerfile(text: str):
    tokens = tokenize(text)
    parser = Parser(tokens)
    return parser.parse()


if __name__ == "__main__":
    import sys
    import json

    with open(sys.argv[1], "r") as f:
        content = f.read()

    ast = parse_dockerfile(content)
    print(json.dumps(ast, indent=2))
