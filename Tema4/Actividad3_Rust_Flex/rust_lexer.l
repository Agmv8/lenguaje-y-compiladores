%{
#include <stdio.h>
%}

%option noyywrap

DIGITO        [0-9]
LETRA         [a-zA-Z_]
IDENTIFICADOR {LETRA}({LETRA}|{DIGITO})*
ENTERO        {DIGITO}+
FLOTANTE      {DIGITO}+\.{DIGITO}+

%%

"fn"          { printf("TOKEN: PALABRA_RESERVADA, Lexema: %s\n", yytext); }
"let"         { printf("TOKEN: PALABRA_RESERVADA, Lexema: %s\n", yytext); }
"mut"         { printf("TOKEN: PALABRA_RESERVADA, Lexema: %s\n", yytext); }
"if"          { printf("TOKEN: PALABRA_RESERVADA, Lexema: %s\n", yytext); }
"else"        { printf("TOKEN: PALABRA_RESERVADA, Lexema: %s\n", yytext); }
"loop"        { printf("TOKEN: PALABRA_RESERVADA, Lexema: %s\n", yytext); }
"return"      { printf("TOKEN: PALABRA_RESERVADA, Lexema: %s\n", yytext); }
"struct"      { printf("TOKEN: PALABRA_RESERVADA, Lexema: %s\n", yytext); }

{FLOTANTE}    { printf("TOKEN: NUMERO_FLOTANTE, Lexema: %s\n", yytext); }
{ENTERO}      { printf("TOKEN: NUMERO_ENTERO, Lexema: %s\n", yytext); }
{IDENTIFICADOR} { printf("TOKEN: IDENTIFICADOR, Lexema: %s\n", yytext); }

"//"([^"\n"])*                  { /* Ignorar comentarios de una linea */ }
"/*"([^*]|\*+[^*/])*\*+"/"      { /* Ignorar comentarios de bloque */ }

"{"           { printf("TOKEN: LLAVE_ABIERTA, Lexema: %s\n", yytext); }
"}"           { printf("TOKEN: LLAVE_CERRADA, Lexema: %s\n", yytext); }
"("           { printf("TOKEN: PARENTESIS_ABIERTO, Lexema: %s\n", yytext); }
")"           { printf("TOKEN: PARENTESIS_CERRADO, Lexema: %s\n", yytext); }
";"           { printf("TOKEN: FIN_SENTENCIA, Lexema: %s\n", yytext); }
"="           { printf("TOKEN: OPERADOR_ASIGNACION, %s\n", yytext); }

[ \t\n\r]+    { /* Ignorar espacios en blanco */ }
.             { printf("ERROR LEXICO: Caracter no reconocido: %s\n", yytext); }

%%

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("Error al abrir archivo");
            return 1;
        }
        yyin = file;
    }
    yylex();
    return 0;
}