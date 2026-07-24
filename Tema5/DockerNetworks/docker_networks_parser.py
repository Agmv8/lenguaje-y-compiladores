import re
import sys

# =====================================================================
# Definición de Tokens y Nodos AST
# =====================================================================

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, Line:{self.line}, Col:{self.column})"


class ASTNode:
    def to_dict(self):
        raise NotImplementedError()

    def __str__(self):
        import json
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class NetworksSectionNode(ASTNode):
    def __init__(self, networks):
        self.networks = networks  # List of NetworkDefinitionNode

    def to_dict(self):
        return {
            "type": "NetworksSection",
            "networks": [net.to_dict() for net in self.networks]
        }


class NetworkDefinitionNode(ASTNode):
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties  # List of PropertyNode

    def to_dict(self):
        return {
            "type": "NetworkDefinition",
            "name": self.name,
            "properties": [prop.to_dict() for prop in self.properties]
        }


class PropertyNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_dict(self):
        val_repr = self.value.to_dict() if isinstance(self.value, ASTNode) else self.value
        return {
            "type": "Property",
            "name": self.name,
            "value": val_repr
        }


class IPAMNode(ASTNode):
    def __init__(self, properties):
        self.properties = properties  # List of PropertyNode (driver, config, etc.)

    def to_dict(self):
        return {
            "type": "IPAMConfiguration",
            "properties": [prop.to_dict() for prop in self.properties]
        }


class IPAMConfigListNode(ASTNode):
    def __init__(self, items):
        self.items = items  # List of dicts/PropertyNodes

    def to_dict(self):
        return {
            "type": "IPAMConfigList",
            "items": self.items
        }


class ExternalNode(ASTNode):
    def __init__(self, value):
        # value can be a boolean (e.g. True) or a list of properties (like name: string)
        self.value = value

    def to_dict(self):
        if isinstance(self.value, bool):
            val_representation = self.value
        else:
            val_representation = [prop.to_dict() for prop in self.value]
        return {
            "type": "ExternalConfiguration",
            "value": val_representation
        }


# =====================================================================
# Analizador Léxico (Lexer)
# =====================================================================

class DockerNetworksLexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.line_num = 1
        self.indent_stack = [0]

    def tokenize(self):
        lines = self.text.split('\n')
        
        for idx, line in enumerate(lines):
            self.line_num = idx + 1
            
            # 1. Limpieza de comentarios y espacios finales
            # Buscamos el caracter # que no esté dentro de una cadena
            # Para simplificar, si hay un #, cortamos la línea ahí a menos que esté entre comillas.
            # Implementamos una limpieza básica de comentarios:
            clean_line = ""
            in_quotes = False
            quote_char = None
            for char in line:
                if char in ('"', "'"):
                    if not in_quotes:
                        in_quotes = True
                        quote_char = char
                    elif char == quote_char:
                        in_quotes = False
                        quote_char = None
                elif char == '#' and not in_quotes:
                    break
                clean_line += char
            
            stripped_line = clean_line.strip()
            
            # Si la línea queda vacía, la ignoramos
            if not stripped_line:
                continue
            
            # 2. Calcular nivel de indentación
            # Contamos los espacios iniciales en la línea limpia de comentarios
            indent = len(clean_line) - len(clean_line.lstrip())
            
            # 3. Emitir tokens de INDENT / DEDENT si corresponde
            current_indent = self.indent_stack[-1]
            if indent > current_indent:
                self.indent_stack.append(indent)
                self.tokens.append(Token('INDENT', indent, self.line_num, indent))
            elif indent < current_indent:
                while indent < self.indent_stack[-1]:
                    old_indent = self.indent_stack.pop()
                    # El valor del DEDENT es el nivel al que regresamos
                    self.tokens.append(Token('DEDENT', self.indent_stack[-1], self.line_num, indent))
                if indent != self.indent_stack[-1]:
                    raise SyntaxError(
                        f"Error de indentación en línea {self.line_num}: "
                        f"Nivel de espacios ({indent}) no coincide con ningún nivel anterior."
                    )
            
            # 4. Tokenizar el contenido de la línea
            # Procesamos secuencialmente con expresiones regulares
            line_text = clean_line.lstrip()
            col = indent
            
            # Expresiones regulares para los componentes
            # Clave inicial 'networks:'
            networks_regex = re.compile(r'^networks(?=\s*:)')
            # Dirección IP (soporta IPv4 con o sin máscara /CIDR y patrones simples)
            ip_regex = re.compile(r'^\b\d{1,3}(?:\.\d{1,3}){3}(?:/\d{1,2})?\b')
            # Valores booleanos
            bool_regex = re.compile(r'^\b(true|false|yes|no)\b', re.IGNORECASE)
            # Números
            num_regex = re.compile(r'^\b\d+(?:\.\d+)?\b')
            # Cadenas entre comillas
            str_regex = re.compile(r'^("[^"]*"|\'[^\']*\')')
            # Palabras clave específicas
            keywords = {
                'driver': 'DRIVER',
                'ipam': 'IPAM',
                'config': 'CONFIG',
                'subnet': 'SUBNET',
                'gateway': 'GATEWAY',
                'external': 'EXTERNAL',
                'attachable': 'ATTACHABLE',
                'enable_ipv6': 'ENABLE_IPV6'
            }
            # Identificadores y guiones
            id_regex = re.compile(r'^[a-zA-Z0-9_\-]+')
            
            while line_text:
                # Saltar espacios intermedios
                spaces_match = re.match(r'^[ \t\r]+', line_text)
                if spaces_match:
                    length = len(spaces_match.group(0))
                    line_text = line_text[length:]
                    col += length
                    continue
                
                # Match networks
                m = networks_regex.match(line_text)
                if m:
                    val = m.group(0)
                    self.tokens.append(Token('NETWORKS', val, self.line_num, col))
                    length = len(val)
                    line_text = line_text[length:]
                    col += length
                    continue
                
                # Match IP
                m = ip_regex.match(line_text)
                if m:
                    val = m.group(0)
                    self.tokens.append(Token('IP_ADDRESS', val, self.line_num, col))
                    length = len(val)
                    line_text = line_text[length:]
                    col += length
                    continue
                
                # Match Boolean
                m = bool_regex.match(line_text)
                if m:
                    val = m.group(0)
                    self.tokens.append(Token('BOOLEAN', val, self.line_num, col))
                    length = len(val)
                    line_text = line_text[length:]
                    col += length
                    continue
                
                # Match Number
                m = num_regex.match(line_text)
                if m:
                    val = m.group(0)
                    self.tokens.append(Token('NUMBER', val, self.line_num, col))
                    length = len(val)
                    line_text = line_text[length:]
                    col += length
                    continue
                
                # Match Quoted String
                m = str_regex.match(line_text)
                if m:
                    val = m.group(0)
                    # Quitar comillas
                    content = val[1:-1]
                    self.tokens.append(Token('STRING', content, self.line_num, col))
                    length = len(val)
                    line_text = line_text[length:]
                    col += length
                    continue
                
                # Match colon
                if line_text.startswith(':'):
                    self.tokens.append(Token('COLON', ':', self.line_num, col))
                    line_text = line_text[1:]
                    col += 1
                    continue
                
                # Match dash (para listas)
                if line_text.startswith('-'):
                    self.tokens.append(Token('DASH', '-', self.line_num, col))
                    line_text = line_text[1:]
                    col += 1
                    continue
                
                # Match Identifier & Keywords
                m = id_regex.match(line_text)
                if m:
                    val = m.group(0)
                    token_type = keywords.get(val.lower(), 'IDENTIFIER')
                    self.tokens.append(Token(token_type, val, self.line_num, col))
                    length = len(val)
                    line_text = line_text[length:]
                    col += length
                    continue
                
                # Si llegamos aquí, hay un carácter no reconocido (Error Léxico)
                err_char = line_text[0]
                raise RuntimeError(
                    f"Error Léxico en línea {self.line_num}, columna {col}: "
                    f"Carácter no reconocido {err_char!r}."
                )
            
            # Al final de la línea con contenido, emitimos NEWLINE
            self.tokens.append(Token('NEWLINE', '\n', self.line_num, col))

        # Al terminar de leer el archivo, cerramos las indentaciones pendientes
        while len(self.indent_stack) > 1:
            old_indent = self.indent_stack.pop()
            self.tokens.append(Token('DEDENT', self.indent_stack[-1], self.line_num + 1, 0))
            
        self.tokens.append(Token('EOF', '', self.line_num + 1, 0))
        return self.tokens


# =====================================================================
# Excepción del Parser y Recuperación de Errores
# =====================================================================

class ParserError(Exception):
    def __init__(self, message, token):
        super().__init__(message)
        self.token = token


# =====================================================================
# Analizador Sintáctico (Parser)
# =====================================================================

class DockerNetworksParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def current_token(self):
        return self.tokens[self.pos]

    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return self.tokens[self.pos]

    def match(self, expected_type):
        tok = self.current_token()
        if tok.type == expected_type:
            self.advance()
            return tok
        else:
            raise ParserError(
                f"Error Sintáctico: Se esperaba un token de tipo '{expected_type}', "
                f"pero se obtuvo '{tok.type}' ('{tok.value}').", 
                tok
            )

    def parse_value(self):
        tok = self.current_token()
        valid_types = ('IDENTIFIER', 'STRING', 'BOOLEAN', 'NUMBER', 'IP_ADDRESS')
        if tok.type in valid_types:
            self.advance()
            return tok
        else:
            raise ParserError(
                f"Error Sintáctico: Se esperaba un valor (identificador, cadena, booleano, número o IP), "
                f"pero se obtuvo '{tok.type}' ('{tok.value}').", 
                tok
            )

    # -----------------------------------------------------------------
    # Recuperación de Errores (Modo Pánico)
    # -----------------------------------------------------------------
    def recover_to_network_level(self):
        """
        Descarta tokens hasta encontrar un punto de sincronización estable:
        - Un DEDENT que vuelva al nivel de la lista de redes (indentación 2).
        - Un DEDENT final que cierre la sección (indentación 0).
        - El inicio de una nueva red (un IDENTIFIER en columna 2, precedido por NEWLINE).
        - EOF (fin de archivo).
        """
        while self.pos < len(self.tokens):
            tok = self.tokens[self.pos]
            if tok.type == 'EOF':
                break
            
            # Sincronización mediante DEDENT de retorno al nivel 2 o 0
            if tok.type == 'DEDENT' and tok.value in (2, 0):
                self.pos += 1  # Consumir el DEDENT para quedar al nivel de la red o sección
                break
            
            # Sincronización mediante el nombre de otra red (IDENTIFIER en la columna 2 tras NEWLINE)
            if tok.type == 'IDENTIFIER' and tok.column == 2:
                prev_tok = self.tokens[self.pos - 1] if self.pos > 0 else None
                if prev_tok and prev_tok.type == 'NEWLINE':
                    # Detenerse antes del IDENTIFIER para que parse_network_list pueda procesarlo
                    break
            
            # Continuar descartando
            self.pos += 1

    # -----------------------------------------------------------------
    # Reglas Sintácticas del Parser
    # -----------------------------------------------------------------
    
    def parse(self):
        """
        S -> networks_section EOF
        """
        try:
            # Consumir NEWLINE iniciales que pudieran existir
            while self.current_token().type == 'NEWLINE':
                self.advance()
                
            networks_node = self.parse_networks_section()
            self.match('EOF')
            return networks_node
        except ParserError as e:
            self.errors.append({
                "line": e.token.line,
                "column": e.token.column,
                "msg": str(e)
            })
            return None

    def parse_networks_section(self):
        """
        networks_section -> NETWORKS COLON NEWLINE INDENT network_list DEDENT
        """
        self.match('NETWORKS')
        self.match('COLON')
        self.match('NEWLINE')
        self.match('INDENT')
        
        networks = self.parse_network_list()
        
        self.match('DEDENT')
        return NetworksSectionNode(networks)

    def parse_network_list(self):
        """
        network_list -> network_def (network_def)*
        """
        networks = []
        # El bucle continúa mientras el token actual no sea DEDENT (que cierra la sección de redes)
        # y no sea EOF.
        while self.current_token().type != 'DEDENT' and self.current_token().type != 'EOF':
            # Saltar líneas vacías o NEWLINE huérfanos entre definiciones
            if self.current_token().type == 'NEWLINE':
                self.advance()
                continue
                
            net_def = self.parse_network_def()
            if net_def:
                networks.append(net_def)
                
        return networks

    def parse_network_def(self):
        """
        network_def -> IDENTIFIER COLON NEWLINE INDENT property_list DEDENT
        """
        try:
            net_name_tok = self.match('IDENTIFIER')
            self.match('COLON')
            self.match('NEWLINE')
            self.match('INDENT')
            
            properties = self.parse_property_list()
            
            self.match('DEDENT')
            return NetworkDefinitionNode(net_name_tok.value, properties)
        except ParserError as e:
            # Registrar el error
            self.errors.append({
                "line": e.token.line,
                "column": e.token.column,
                "msg": f"Error al analizar la red: {str(e)}"
            })
            # Aplicar modo pánico: recuperar al nivel del listado de redes
            self.recover_to_network_level()
            return None

    def parse_property_list(self):
        """
        property_list -> property (property)*
        """
        properties = []
        while self.current_token().type != 'DEDENT' and self.current_token().type != 'EOF':
            if self.current_token().type == 'NEWLINE':
                self.advance()
                continue
                
            prop = self.parse_property()
            if prop:
                properties.append(prop)
        return properties

    def parse_property(self):
        """
        property -> simple_prop | ipam_prop | external_prop
        """
        tok = self.current_token()
        
        # Reconocer bloques especiales basados en la palabra clave
        if tok.type == 'IPAM':
            return self.parse_ipam_prop()
        elif tok.type == 'EXTERNAL':
            return self.parse_external_prop()
        else:
            return self.parse_simple_prop()

    def parse_simple_prop(self):
        """
        simple_prop -> IDENTIFIER COLON value NEWLINE
                     | DRIVER COLON value NEWLINE
                     | ATTACHABLE COLON value NEWLINE
                     | ENABLE_IPV6 COLON value NEWLINE
                     | SUBNET COLON value NEWLINE
                     | GATEWAY COLON value NEWLINE
        """
        # Aceptamos palabras clave como identificadores válidos para propiedades simples
        valid_keys = ('IDENTIFIER', 'DRIVER', 'ATTACHABLE', 'ENABLE_IPV6', 'SUBNET', 'GATEWAY')
        tok = self.current_token()
        if tok.type in valid_keys:
            key_name = tok.value
            self.advance()
        else:
            raise ParserError(
                f"Error Sintáctico: Se esperaba una llave de propiedad (como 'driver', 'attachable' o identificador), "
                f"pero se obtuvo '{tok.type}' ('{tok.value}').", 
                tok
            )
            
        self.match('COLON')
        val_token = self.parse_value()
        self.match('NEWLINE')
        
        return PropertyNode(key_name, val_token.value)

    def parse_ipam_prop(self):
        """
        ipam_prop -> IPAM COLON NEWLINE INDENT ipam_body DEDENT
        """
        ipam_tok = self.match('IPAM')
        self.match('COLON')
        self.match('NEWLINE')
        self.match('INDENT')
        
        properties = []
        while self.current_token().type != 'DEDENT' and self.current_token().type != 'EOF':
            if self.current_token().type == 'NEWLINE':
                self.advance()
                continue
                
            # Dentro de IPAM puede haber driver o config
            tok = self.current_token()
            if tok.type == 'CONFIG':
                properties.append(self.parse_config_prop())
            else:
                properties.append(self.parse_simple_prop())
                
        self.match('DEDENT')
        return PropertyNode(ipam_tok.value, IPAMNode(properties))

    def parse_config_prop(self):
        """
        config_prop -> CONFIG COLON NEWLINE INDENT config_list DEDENT
        """
        config_tok = self.match('CONFIG')
        self.match('COLON')
        self.match('NEWLINE')
        self.match('INDENT')
        
        items = []
        while self.current_token().type != 'DEDENT' and self.current_token().type != 'EOF':
            if self.current_token().type == 'NEWLINE':
                self.advance()
                continue
            
            # Cada item de la lista de configuración empieza con un guion DASH
            item_props = self.parse_config_item()
            items.append(item_props)
            
        self.match('DEDENT')
        return PropertyNode(config_tok.value, IPAMConfigListNode(items))

    def parse_config_item(self):
        """
        config_item -> DASH simple_prop (INDENT simple_prop* DEDENT)?
        """
        self.match('DASH')
        
        # El primer elemento está en la misma línea después del guion
        # Esperamos una propiedad simple
        valid_keys = ('IDENTIFIER', 'SUBNET', 'GATEWAY')
        tok = self.current_token()
        if tok.type in valid_keys:
            key_name = tok.value
            self.advance()
        else:
            raise ParserError(
                f"Error Sintáctico: Se esperaba una llave de propiedad de configuración (como 'subnet'), "
                f"pero se obtuvo '{tok.type}' ('{tok.value}').", 
                tok
            )
            
        self.match('COLON')
        val_tok = self.parse_value()
        self.match('NEWLINE')
        
        item_dict = {key_name: val_tok.value}
        
        # Si la siguiente línea tiene un nivel adicional de indentación,
        # significa que hay propiedades adicionales alineadas para este item (ej. gateway)
        if self.current_token().type == 'INDENT':
            self.match('INDENT')
            while self.current_token().type != 'DEDENT' and self.current_token().type != 'EOF':
                if self.current_token().type == 'NEWLINE':
                    self.advance()
                    continue
                # Parsear otra propiedad simple
                sub_tok = self.current_token()
                if sub_tok.type in valid_keys:
                    sub_key = sub_tok.value
                    self.advance()
                else:
                    raise ParserError(
                        f"Error Sintáctico: Se esperaba una propiedad de configuración adicional, "
                        f"pero se obtuvo '{sub_tok.type}' ('{sub_tok.value}').", 
                        sub_tok
                    )
                self.match('COLON')
                sub_val = self.parse_value()
                self.match('NEWLINE')
                item_dict[sub_key] = sub_val.value
                
            self.match('DEDENT')
            
        return item_dict

    def parse_external_prop(self):
        """
        external_prop -> EXTERNAL COLON BOOLEAN NEWLINE
                       | EXTERNAL COLON NEWLINE INDENT property_list DEDENT
        """
        ext_tok = self.match('EXTERNAL')
        self.match('COLON')
        
        # Si sigue un booleano en la misma línea
        if self.current_token().type == 'BOOLEAN':
            val_tok = self.match('BOOLEAN')
            self.match('NEWLINE')
            is_ext = val_tok.value.lower() in ('true', 'yes')
            return PropertyNode(ext_tok.value, ExternalNode(is_ext))
        else:
            # Caso en que es un bloque indentado (ej: external: name: mi-red)
            self.match('NEWLINE')
            self.match('INDENT')
            properties = self.parse_property_list()
            self.match('DEDENT')
            return PropertyNode(ext_tok.value, ExternalNode(properties))


# =====================================================================
# Función de Diagnóstico y Análisis Rápido
# =====================================================================

def analizar_archivo_yaml(filepath):
    print(f"\n" + "="*60)
    print(f" Analizando archivo: {filepath}")
    print(f"="*60)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Archivo no encontrado: {filepath}")
        return False
    except Exception as e:
        print(f"ERROR al abrir el archivo: {e}")
        return False
        
    print("--- Contenido Original ---")
    print(content.strip())
    print("-" * 30)

    # 1. Análisis Léxico
    lexer = DockerNetworksLexer(content)
    try:
        tokens = lexer.tokenize()
        print("\n--> [LÉXICO] Fichas (Tokens) generadas exitosamente:")
        for t in tokens:
            # Ocultamos NEWLINEs y EOFs simples para no saturar la salida, o mostramos todo
            if t.type not in ('NEWLINE', 'EOF'):
                print(f"  {t}")
    except (SyntaxError, RuntimeError) as e:
        print(f"\n[ERROR LÉXICO]: {e}")
        return False

    # 2. Análisis Sintáctico
    parser = DockerNetworksParser(tokens)
    ast = parser.parse()
    
    if parser.errors:
        print(f"\n[SINTÁCTICO] Se detectaron {len(parser.errors)} errores sintácticos:")
        for err in parser.errors:
            print(f"  Línea {err['line']}, Columna {err['column']}: {err['msg']}")
            
        if ast:
            print("\n[ALERTA - SINTÁCTICO] AST Parcial generado tras recuperación de errores (Modo Pánico):")
            print(ast)
        else:
            print("\n[ERROR - SINTÁCTICO] No se pudo generar el AST debido a errores graves.")
        return False
    else:
        print("\n[OK - SINTÁCTICO] Análisis sintáctico completado sin errores.")
        print("\n--> Árbol de Sintaxis Abstracta (AST) generado:")
        print(ast)
        return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        analizar_archivo_yaml(sys.argv[1])
    else:
        print("Uso: python docker_networks_parser.py <ruta_archivo_yaml>")
