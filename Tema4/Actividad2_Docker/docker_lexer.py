import re
import sys
import os

# Definición de los tokens para instrucciones y componentes de Dockerfile
tokens = [
    ('FROM', r'\b(?:FROM|from)\b'),
    ('RUN', r'\b(?:RUN|run)\b'),
    ('COPY', r'\b(?:COPY|copy)\b'),
    ('CMD', r'\b(?:CMD|cmd)\b'),
    ('EXPOSE', r'\b(?:EXPOSE|expose)\b'),
    ('ENV', r'\b(?:ENV|env)\b'),
    ('WORKDIR', r'\b(?:WORKDIR|workdir)\b'),
    ('ARG', r'\b(?:ARG|arg)\b'),
    ('ADD', r'\b(?:ADD|add)\b'),
    ('ENTRYPOINT', r'\b(?:ENTRYPOINT|entrypoint)\b'),
    ('VOLUME', r'\b(?:VOLUME|volume)\b'),
    ('USER', r'\b(?:USER|user)\b'),
    ('LABEL', r'\b(?:LABEL|label)\b'),
    ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
    ('STRING', r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('COMMA', r','),
    ('ASSIGN', r'='),
    ('ARGUMENT', r'[a-zA-Z0-9_\-\.\/\:\@\$\{\}\*\+]+'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t\r]+'),
    ('COMMENT', r'#[^\n]*'),
    ('MISMATCH', r'.'),
]

def lexer(input_text):
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)
    line_num = 1
    line_start = 0
    for mo in re.finditer(token_regex, input_text, re.MULTILINE):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue  # Ignorar espacios, tabulaciones y comentarios
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        else:
            column = mo.start() - line_start
            yield kind, value, line_num, column

def cargar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado. Sorry!")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def analizar_y_mostrar(nombre_archivo):
    print(f"\n==========================================")
    print(f"Analizando archivo: {nombre_archivo}")
    print(f"==========================================\n")
    
    input_text = cargar_archivo(nombre_archivo)
    if input_text is None:
        return
        
    try:
        for token in lexer(input_text):
            print(token)
    except RuntimeError as e:
        print(f"ERROR LÉXICO: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Analizar archivo pasado como argumento
        analizar_y_mostrar(sys.argv[1])
    else:
        # Por defecto, analizar los tres archivos de prueba relativos al directorio del script o ejecutable
        if getattr(sys, 'frozen', False):
            dir_base = os.path.dirname(sys.executable)
        else:
            dir_base = os.path.dirname(os.path.abspath(__file__))
            
        archivos_prueba = [
            os.path.join(dir_base, 'Dockerfile_ejemplo1'),
            os.path.join(dir_base, 'Dockerfile_ejemplo2'),
            os.path.join(dir_base, 'Dockerfile_ejemplo3')
        ]
        for archivo in archivos_prueba:
            analizar_y_mostrar(archivo)
