"""
Lexer para Dockerfile.
Convierte el texto crudo en una lista de líneas lógicas listas para el parser,
resolviendo primero las continuaciones de línea (backslash al final).
"""

INSTRUCTIONS = {
    "FROM", "RUN", "COPY", "ADD", "ENV", "EXPOSE", "WORKDIR", "CMD",
    "ENTRYPOINT", "ARG", "LABEL", "USER", "VOLUME", "STOPSIGNAL",
    "HEALTHCHECK", "SHELL", "MAINTAINER"
}


class Token:
    __slots__ = ("type", "value", "line")

    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


def resolve_line_continuations(text: str):
    """Une líneas terminadas en backslash con la siguiente, devolviendo
    una lista de (numero_de_linea_inicial, texto_logico)."""
    raw_lines = text.split("\n")
    logical_lines = []
    buffer = ""
    start_line = None

    for i, raw in enumerate(raw_lines, start=1):
        if start_line is None:
            start_line = i
        stripped = raw.rstrip()
        if stripped.endswith("\\"):
            buffer += stripped[:-1] + " "
        else:
            buffer += raw
            logical_lines.append((start_line, buffer))
            buffer = ""
            start_line = None

    if buffer:
        logical_lines.append((start_line, buffer))

    return logical_lines


def tokenize_line(line_text: str, line_no: int):
    """Tokeniza una línea lógica ya resuelta (sin continuaciones)."""
    tokens = []
    stripped = line_text.strip()

    if not stripped:
        return tokens  # línea vacía, se ignora

    if stripped.startswith("#"):
        tokens.append(Token("COMMENT", stripped[1:].strip(), line_no))
        return tokens

    parts = stripped.split(None, 1)
    first_word = parts[0]

    if first_word.upper() in INSTRUCTIONS:
        tokens.append(Token("INSTRUCTION", first_word.upper(), line_no))
        rest = parts[1] if len(parts) > 1 else ""
        tokens.extend(tokenize_arguments(rest, line_no))
    else:
        # Instrucción desconocida -> se marca como error léxico
        tokens.append(Token("UNKNOWN", first_word, line_no))

    return tokens


def tokenize_arguments(rest: str, line_no: int):
    tokens = []
    rest = rest.strip()
    if not rest:
        return tokens

    if rest.startswith("["):
        # forma exec: ["a", "b", "c"]
        i = 0
        n = len(rest)
        while i < n:
            c = rest[i]
            if c == "[":
                tokens.append(Token("LBRACKET", "[", line_no))
                i += 1
            elif c == "]":
                tokens.append(Token("RBRACKET", "]", line_no))
                i += 1
            elif c == ",":
                tokens.append(Token("COMMA", ",", line_no))
                i += 1
            elif c == '"':
                j = i + 1
                buf = []
                while j < n and rest[j] != '"':
                    buf.append(rest[j])
                    j += 1
                tokens.append(Token("STRING", "".join(buf), line_no))
                i = j + 1
            else:
                i += 1  # espacios u otros separadores
        return tokens

    # forma shell / key=value / texto plano
    for word in rest.split():
        if "=" in word:
            key, _, value = word.partition("=")
            tokens.append(Token("IDENTIFIER", key, line_no))
            tokens.append(Token("EQUALS", "=", line_no))
            if value.startswith('"') and value.endswith('"'):
                tokens.append(Token("STRING", value[1:-1], line_no))
            else:
                tokens.append(Token("IDENTIFIER", value, line_no))
        else:
            tokens.append(Token("IDENTIFIER", word, line_no))

    return tokens


def tokenize(text: str):
    """Punto de entrada: texto crudo -> lista de tokens (con NEWLINE por línea)."""
    all_tokens = []
    for line_no, logical_line in resolve_line_continuations(text):
        line_tokens = tokenize_line(logical_line, line_no)
        if line_tokens:
            all_tokens.extend(line_tokens)
            all_tokens.append(Token("NEWLINE", "\n", line_no))
    all_tokens.append(Token("EOF", None, -1))
    return all_tokens
