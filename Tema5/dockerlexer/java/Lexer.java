package dockerlexer;

import java.util.*;

/**
 * Lexer para Dockerfile.
 * Convierte el texto crudo en una lista de tokens, resolviendo primero
 * las continuaciones de linea (backslash al final).
 */
public class Lexer {

    static final Set<String> INSTRUCTIONS = new HashSet<>(Arrays.asList(
        "FROM", "RUN", "COPY", "ADD", "ENV", "EXPOSE", "WORKDIR", "CMD",
        "ENTRYPOINT", "ARG", "LABEL", "USER", "VOLUME", "STOPSIGNAL",
        "HEALTHCHECK", "SHELL", "MAINTAINER"
    ));

    public enum TokenType {
        INSTRUCTION, COMMENT, STRING, IDENTIFIER, EQUALS,
        LBRACKET, RBRACKET, COMMA, NEWLINE, UNKNOWN, EOF
    }

    public static class Token {
        public final TokenType type;
        public final String value;
        public final int line;

        public Token(TokenType type, String value, int line) {
            this.type = type;
            this.value = value;
            this.line = line;
        }

        @Override
        public String toString() {
            return "Token(" + type + ", " + value + ")";
        }
    }

    /** Une lineas terminadas en backslash con la siguiente. */
    static List<int[]> lineStarts; // no usado, placeholder para claridad

    static List<Map.Entry<Integer, String>> resolveLineContinuations(String text) {
        String[] rawLines = text.split("\n", -1);
        List<Map.Entry<Integer, String>> logicalLines = new ArrayList<>();
        StringBuilder buffer = new StringBuilder();
        int startLine = -1;

        for (int i = 0; i < rawLines.length; i++) {
            int lineNo = i + 1;
            if (startLine == -1) startLine = lineNo;
            String raw = rawLines[i];
            String trimmedEnd = stripTrailing(raw);

            if (trimmedEnd.endsWith("\\")) {
                buffer.append(trimmedEnd, 0, trimmedEnd.length() - 1).append(" ");
            } else {
                buffer.append(raw);
                logicalLines.add(new AbstractMap.SimpleEntry<>(startLine, buffer.toString()));
                buffer.setLength(0);
                startLine = -1;
            }
        }

        if (buffer.length() > 0) {
            logicalLines.add(new AbstractMap.SimpleEntry<>(startLine, buffer.toString()));
        }

        return logicalLines;
    }

    static String stripTrailing(String s) {
        int end = s.length();
        while (end > 0 && Character.isWhitespace(s.charAt(end - 1))) end--;
        return s.substring(0, end);
    }

    static List<Token> tokenizeLine(String lineText, int lineNo) {
        List<Token> tokens = new ArrayList<>();
        String stripped = lineText.strip();

        if (stripped.isEmpty()) return tokens;

        if (stripped.startsWith("#")) {
            tokens.add(new Token(TokenType.COMMENT, stripped.substring(1).strip(), lineNo));
            return tokens;
        }

        int spaceIdx = indexOfWhitespace(stripped);
        String firstWord = spaceIdx == -1 ? stripped : stripped.substring(0, spaceIdx);
        String rest = spaceIdx == -1 ? "" : stripped.substring(spaceIdx).strip();

        if (INSTRUCTIONS.contains(firstWord.toUpperCase())) {
            tokens.add(new Token(TokenType.INSTRUCTION, firstWord.toUpperCase(), lineNo));
            tokens.addAll(tokenizeArguments(rest, lineNo));
        } else {
            tokens.add(new Token(TokenType.UNKNOWN, firstWord, lineNo));
        }

        return tokens;
    }

    static int indexOfWhitespace(String s) {
        for (int i = 0; i < s.length(); i++) {
            if (Character.isWhitespace(s.charAt(i))) return i;
        }
        return -1;
    }

    static List<Token> tokenizeArguments(String rest, int lineNo) {
        List<Token> tokens = new ArrayList<>();
        rest = rest.strip();
        if (rest.isEmpty()) return tokens;

        if (rest.startsWith("[")) {
            int i = 0, n = rest.length();
            while (i < n) {
                char c = rest.charAt(i);
                if (c == '[') {
                    tokens.add(new Token(TokenType.LBRACKET, "[", lineNo));
                    i++;
                } else if (c == ']') {
                    tokens.add(new Token(TokenType.RBRACKET, "]", lineNo));
                    i++;
                } else if (c == ',') {
                    tokens.add(new Token(TokenType.COMMA, ",", lineNo));
                    i++;
                } else if (c == '"') {
                    int j = i + 1;
                    StringBuilder buf = new StringBuilder();
                    while (j < n && rest.charAt(j) != '"') {
                        buf.append(rest.charAt(j));
                        j++;
                    }
                    tokens.add(new Token(TokenType.STRING, buf.toString(), lineNo));
                    i = j + 1;
                } else {
                    i++;
                }
            }
            return tokens;
        }

        for (String word : rest.split("\\s+")) {
            if (word.isEmpty()) continue;
            if (word.contains("=")) {
                int eq = word.indexOf('=');
                String key = word.substring(0, eq);
                String value = word.substring(eq + 1);
                tokens.add(new Token(TokenType.IDENTIFIER, key, lineNo));
                tokens.add(new Token(TokenType.EQUALS, "=", lineNo));
                if (value.startsWith("\"") && value.endsWith("\"") && value.length() >= 2) {
                    tokens.add(new Token(TokenType.STRING, value.substring(1, value.length() - 1), lineNo));
                } else {
                    tokens.add(new Token(TokenType.IDENTIFIER, value, lineNo));
                }
            } else {
                tokens.add(new Token(TokenType.IDENTIFIER, word, lineNo));
            }
        }

        return tokens;
    }

    public static List<Token> tokenize(String text) {
        List<Token> allTokens = new ArrayList<>();
        for (Map.Entry<Integer, String> entry : resolveLineContinuations(text)) {
            List<Token> lineTokens = tokenizeLine(entry.getValue(), entry.getKey());
            if (!lineTokens.isEmpty()) {
                allTokens.addAll(lineTokens);
                allTokens.add(new Token(TokenType.NEWLINE, "\n", entry.getKey()));
            }
        }
        allTokens.add(new Token(TokenType.EOF, null, -1));
        return allTokens;
    }
}
