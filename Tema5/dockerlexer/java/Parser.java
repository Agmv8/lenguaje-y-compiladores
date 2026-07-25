package dockerlexer;

import java.util.*;
import dockerlexer.Lexer.Token;
import dockerlexer.Lexer.TokenType;

/**
 * Parser para Dockerfile. Consume los tokens del Lexer y construye un AST
 * como lista de nodos (Map), siguiendo la misma gramatica que las demas
 * implementaciones (Python, Rust).
 */
public class Parser {

    public static class ParseException extends RuntimeException {
        public ParseException(String msg) { super(msg); }
    }

    public static class Node {
        public String instruction;
        public List<String> args = new ArrayList<>();
        public String form; // puede ser null

        public String toJson() {
            StringBuilder sb = new StringBuilder();
            sb.append("{");
            sb.append("\"instruction\": \"").append(escape(instruction)).append("\", ");
            sb.append("\"args\": [");
            for (int i = 0; i < args.size(); i++) {
                if (i > 0) sb.append(", ");
                sb.append("\"").append(escape(args.get(i))).append("\"");
            }
            sb.append("]");
            if (form != null) {
                sb.append(", \"form\": \"").append(escape(form)).append("\"");
            }
            sb.append("}");
            return sb.toString();
        }

        static String escape(String s) {
            if (s == null) return "";
            return s.replace("\\", "\\\\").replace("\"", "\\\"");
        }
    }

    private final List<Token> tokens;
    private int pos = 0;

    public Parser(List<Token> tokens) {
        this.tokens = tokens;
    }

    private Token peek() {
        return tokens.get(pos);
    }

    private Token advance() {
        return tokens.get(pos++);
    }

    public List<Node> parse() {
        List<Node> ast = new ArrayList<>();
        boolean seenFrom = false;

        while (peek().type != TokenType.EOF) {
            Token tok = peek();

            if (tok.type == TokenType.COMMENT) {
                advance();
                expectOptionalNewline();
                continue;
            }

            if (tok.type == TokenType.UNKNOWN) {
                throw new ParseException(
                    "Instruccion desconocida '" + tok.value + "' en linea " + tok.line);
            }

            if (tok.type == TokenType.INSTRUCTION) {
                Node node = parseInstruction();
                if (node.instruction.equals("FROM")) {
                    seenFrom = true;
                } else if (!seenFrom && !node.instruction.equals("ARG")) {
                    throw new ParseException(
                        "La instruccion '" + node.instruction + "' aparece antes de FROM (linea "
                        + tok.line + ")");
                }
                ast.add(node);
                continue;
            }

            if (tok.type == TokenType.NEWLINE) {
                advance();
                continue;
            }

            throw new ParseException("Token inesperado " + tok.type + " en linea " + tok.line);
        }

        return ast;
    }

    private void expectOptionalNewline() {
        if (peek().type == TokenType.NEWLINE) advance();
    }

    private Node parseInstruction() {
        Token instrTok = advance();
        Node node = new Node();
        node.instruction = instrTok.value;

        if (peek().type == TokenType.LBRACKET) {
            parseExecForm(node);
        } else {
            parseShellOrKvForm(node);
        }

        expectOptionalNewline();
        return node;
    }

    private void parseExecForm(Node node) {
        advance(); // consume '['
        while (peek().type != TokenType.RBRACKET) {
            Token tok = peek();
            if (tok.type == TokenType.STRING) {
                node.args.add(tok.value);
                advance();
            } else if (tok.type == TokenType.COMMA) {
                advance();
            } else if (tok.type == TokenType.NEWLINE) {
                advance();
            } else {
                throw new ParseException(
                    "Token inesperado " + tok.type + " dentro de forma exec, linea " + tok.line);
            }
        }
        advance(); // consume ']'
        node.form = "exec";
    }

    private void parseShellOrKvForm(Node node) {
        boolean isKv = false;

        while (peek().type == TokenType.IDENTIFIER
                || peek().type == TokenType.EQUALS
                || peek().type == TokenType.STRING) {
            Token tok = advance();
            if (tok.type == TokenType.EQUALS) {
                isKv = true;
                continue;
            }
            node.args.add(tok.value);
        }

        node.form = isKv ? "key_value" : "shell";
    }

    public static List<Node> parseDockerfile(String text) {
        List<Token> tokens = Lexer.tokenize(text);
        Parser parser = new Parser(tokens);
        return parser.parse();
    }
}
