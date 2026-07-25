// Parser para Dockerfile. Consume los tokens de lexer.rs y construye un
// AST como lista de nodos, siguiendo la misma gramatica que las demas
// implementaciones (Python, Java).

use crate::lexer::{tokenize, Token, TokenType};

#[derive(Debug)]
pub struct Node {
    pub instruction: String,
    pub args: Vec<String>,
    pub form: Option<String>,
}

impl Node {
    pub fn to_json(&self) -> String {
        let args_json: Vec<String> = self
            .args
            .iter()
            .map(|a| format!("\"{}\"", escape(a)))
            .collect();

        let mut s = format!(
            "{{\"instruction\": \"{}\", \"args\": [{}]",
            escape(&self.instruction),
            args_json.join(", ")
        );

        if let Some(form) = &self.form {
            s.push_str(&format!(", \"form\": \"{}\"", escape(form)));
        }

        s.push('}');
        s
    }
}

fn escape(s: &str) -> String {
    s.replace('\\', "\\\\").replace('"', "\\\"")
}

#[derive(Debug)]
pub struct ParseError(pub String);

pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Parser { tokens, pos: 0 }
    }

    fn peek(&self) -> &Token {
        &self.tokens[self.pos]
    }

    fn advance(&mut self) -> Token {
        let tok = self.tokens[self.pos].clone();
        self.pos += 1;
        tok
    }

    pub fn parse(&mut self) -> Result<Vec<Node>, ParseError> {
        let mut ast = Vec::new();
        let mut seen_from = false;

        while self.peek().ttype != TokenType::Eof {
            let tok = self.peek().clone();

            match tok.ttype {
                TokenType::Comment => {
                    self.advance();
                    self.expect_optional_newline();
                    continue;
                }
                TokenType::Unknown => {
                    return Err(ParseError(format!(
                        "Instruccion desconocida '{}' en linea {}",
                        tok.value, tok.line
                    )));
                }
                TokenType::Instruction => {
                    let node = self.parse_instruction()?;
                    if node.instruction == "FROM" {
                        seen_from = true;
                    } else if !seen_from && node.instruction != "ARG" {
                        return Err(ParseError(format!(
                            "La instruccion '{}' aparece antes de FROM (linea {})",
                            node.instruction, tok.line
                        )));
                    }
                    ast.push(node);
                    continue;
                }
                TokenType::Newline => {
                    self.advance();
                    continue;
                }
                _ => {
                    return Err(ParseError(format!(
                        "Token inesperado {:?} en linea {}",
                        tok.ttype, tok.line
                    )));
                }
            }
        }

        Ok(ast)
    }

    fn expect_optional_newline(&mut self) {
        if self.peek().ttype == TokenType::Newline {
            self.advance();
        }
    }

    fn parse_instruction(&mut self) -> Result<Node, ParseError> {
        let instr_tok = self.advance();
        let mut node = Node {
            instruction: instr_tok.value,
            args: Vec::new(),
            form: None,
        };

        if self.peek().ttype == TokenType::LBracket {
            self.parse_exec_form(&mut node)?;
        } else {
            self.parse_shell_or_kv_form(&mut node);
        }

        self.expect_optional_newline();
        Ok(node)
    }

    fn parse_exec_form(&mut self, node: &mut Node) -> Result<(), ParseError> {
        self.advance(); // consume '['
        while self.peek().ttype != TokenType::RBracket {
            let tok = self.peek().clone();
            match tok.ttype {
                TokenType::String => {
                    node.args.push(tok.value);
                    self.advance();
                }
                TokenType::Comma | TokenType::Newline => {
                    self.advance();
                }
                _ => {
                    return Err(ParseError(format!(
                        "Token inesperado {:?} dentro de forma exec, linea {}",
                        tok.ttype, tok.line
                    )));
                }
            }
        }
        self.advance(); // consume ']'
        node.form = Some("exec".to_string());
        Ok(())
    }

    fn parse_shell_or_kv_form(&mut self, node: &mut Node) {
        let mut is_kv = false;

        loop {
            match self.peek().ttype {
                TokenType::Identifier | TokenType::Equals | TokenType::String => {
                    let tok = self.advance();
                    if tok.ttype == TokenType::Equals {
                        is_kv = true;
                        continue;
                    }
                    node.args.push(tok.value);
                }
                _ => break,
            }
        }

        node.form = Some(if is_kv { "key_value".to_string() } else { "shell".to_string() });
    }
}

pub fn parse_dockerfile(text: &str) -> Result<Vec<Node>, ParseError> {
    let tokens = tokenize(text);
    let mut parser = Parser::new(tokens);
    parser.parse()
}
