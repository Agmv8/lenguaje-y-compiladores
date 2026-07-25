mod lexer;
mod parser;

use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Uso: {} <archivo.dockerfile>", args[0]);
        process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).unwrap_or_else(|e| {
        eprintln!("Error leyendo archivo: {}", e);
        process::exit(1);
    });

    match parser::parse_dockerfile(&content) {
        Ok(ast) => {
            let items: Vec<String> = ast.iter().map(|n| format!("  {}", n.to_json())).collect();
            println!("[\n{}\n]", items.join(",\n"));
        }
        Err(e) => {
            eprintln!("Error de parseo: {}", e.0);
            process::exit(1);
        }
    }
}
