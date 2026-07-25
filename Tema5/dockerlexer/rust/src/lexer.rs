// Lexer para Dockerfile.
// Convierte el texto crudo en una lista de tokens, resolviendo primero
// las continuaciones de linea (backslash al final).

#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {
    Instruction,
    Comment,
    String,
    Identifier,
    Equals,
    LBracket,
    RBracket,
    Comma,
    Newline,
    Unknown,
    Eof,
}

#[derive(Debug, Clone)]
pub struct Token {
    pub ttype: TokenType,
    pub value: String,
    pub line: i32,
}

const INSTRUCTIONS: &[&str] = &[
    "FROM", "RUN", "COPY", "ADD", "ENV", "EXPOSE", "WORKDIR", "CMD",
    "ENTRYPOINT", "ARG", "LABEL", "USER", "VOLUME", "STOPSIGNAL",
    "HEALTHCHECK", "SHELL", "MAINTAINER",
];

fn is_instruction(word: &str) -> bool {
    let upper = word.to_uppercase();
    INSTRUCTIONS.contains(&upper.as_str())
}

/// Une lineas terminadas en backslash con la siguiente.
/// Devuelve pares (numero_de_linea_inicial, texto_logico).
fn resolve_line_continuations(text: &str) -> Vec<(i32, String)> {
    let raw_lines: Vec<&str> = text.split('\n').collect();
    let mut logical_lines = Vec::new();
    let mut buffer = String::new();
    let mut start_line: i32 = -1;

    for (i, raw) in raw_lines.iter().enumerate() {
        let line_no = (i + 1) as i32;
        if start_line == -1 {
            start_line = line_no;
        }
        let trimmed_end = raw.trim_end();

        if trimmed_end.ends_with('\\') {
            buffer.push_str(&trimmed_end[..trimmed_end.len() - 1]);
            buffer.push(' ');
        } else {
            buffer.push_str(raw);
            logical_lines.push((start_line, buffer.clone()));
            buffer.clear();
            start_line = -1;
        }
    }

    if !buffer.is_empty() {
        logical_lines.push((start_line, buffer.clone()));
    }

    logical_lines
}

fn tokenize_line(line_text: &str, line_no: i32) -> Vec<Token> {
    let mut tokens = Vec::new();
    let stripped = line_text.trim();

    if stripped.is_empty() {
        return tokens;
    }

    if let Some(rest) = stripped.strip_prefix('#') {
        tokens.push(Token {
            ttype: TokenType::Comment,
            value: rest.trim().to_string(),
            line: line_no,
        });
        return tokens;
    }

    let mut parts = stripped.splitn(2, char::is_whitespace);
    let first_word = parts.next().unwrap_or("");
    let rest = parts.next().unwrap_or("").trim();

    if is_instruction(first_word) {
        tokens.push(Token {
            ttype: TokenType::Instruction,
            value: first_word.to_uppercase(),
            line: line_no,
        });
        tokens.extend(tokenize_arguments(rest, line_no));
    } else {
        tokens.push(Token {
            ttype: TokenType::Unknown,
            value: first_word.to_string(),
            line: line_no,
        });
    }

    tokens
}

fn tokenize_arguments(rest: &str, line_no: i32) -> Vec<Token> {
    let mut tokens = Vec::new();
    let rest = rest.trim();
    if rest.is_empty() {
        return tokens;
    }

    if rest.starts_with('[') {
        let chars: Vec<char> = rest.chars().collect();
        let n = chars.len();
        let mut i = 0;
        while i < n {
            let c = chars[i];
            match c {
                '[' => {
                    tokens.push(Token { ttype: TokenType::LBracket, value: "[".to_string(), line: line_no });
                    i += 1;
                }
                ']' => {
                    tokens.push(Token { ttype: TokenType::RBracket, value: "]".to_string(), line: line_no });
                    i += 1;
                }
                ',' => {
                    tokens.push(Token { ttype: TokenType::Comma, value: ",".to_string(), line: line_no });
                    i += 1;
                }
                '"' => {
                    let mut j = i + 1;
                    let mut buf = String::new();
                    while j < n && chars[j] != '"' {
                        buf.push(chars[j]);
                        j += 1;
                    }
                    tokens.push(Token { ttype: TokenType::String, value: buf, line: line_no });
                    i = j + 1;
                }
                _ => {
                    i += 1;
                }
            }
        }
        return tokens;
    }

    for word in rest.split_whitespace() {
        if let Some(eq_idx) = word.find('=') {
            let key = &word[..eq_idx];
            let value = &word[eq_idx + 1..];
            tokens.push(Token { ttype: TokenType::Identifier, value: key.to_string(), line: line_no });
            tokens.push(Token { ttype: TokenType::Equals, value: "=".to_string(), line: line_no });
            if value.starts_with('"') && value.ends_with('"') && value.len() >= 2 {
                tokens.push(Token {
                    ttype: TokenType::String,
                    value: value[1..value.len() - 1].to_string(),
                    line: line_no,
                });
            } else {
                tokens.push(Token { ttype: TokenType::Identifier, value: value.to_string(), line: line_no });
            }
        } else {
            tokens.push(Token { ttype: TokenType::Identifier, value: word.to_string(), line: line_no });
        }
    }

    tokens
}

pub fn tokenize(text: &str) -> Vec<Token> {
    let mut all_tokens = Vec::new();
    for (line_no, logical_line) in resolve_line_continuations(text) {
        let line_tokens = tokenize_line(&logical_line, line_no);
        if !line_tokens.is_empty() {
            all_tokens.extend(line_tokens);
            all_tokens.push(Token { ttype: TokenType::Newline, value: "\n".to_string(), line: line_no });
        }
    }
    all_tokens.push(Token { ttype: TokenType::Eof, value: String::new(), line: -1 });
    all_tokens
}
