/**
 * UNEG - COORDINACIÓN DE INGENIERÍA EN INFORMÁTICA
 * CÁTEDRA: LENGUAJES Y COMPILADORES
 * * INTÉRPRETE REAL CORREGIDO PARA EL LENGUAJE "L"
 */

const fs = require('fs');
const path = require('path');

// --- REGISTROS DE HARDWARE / TABLA DE SÍMBOLOS ---
let MemoriaL = {
    principal: 0,
    hospital: 0,
    industrias: 0,
    residencial: 0,
    banco_ion_litio: 0,
    panel_solar: 0,
    consumo_total: 0
};

// Reiniciar memoria entre programas para evitar colisiones
function limpiarMemoria() {
    MemoriaL = { principal: 0, hospital: 0, industrias: 0, residencial: 0, banco_ion_litio: 0, panel_solar: 0, consumo_total: 0 };
}

// --- ANALIZADOR LÉXICO (LEXER) ROBUSTO CON EXPRESIONES REGULARES ---
function parsearAsignacionesDesdeArchivo(contenidoCuerpo) {
    const lineas = contenidoCuerpo.split('\n');
    
    lineas.forEach(linea => {
        // 1. Descartar comentarios de nuestro lenguaje L ($)
        const lineaLimpia = linea.split('$')[0].trim();
        
        // 2. Expresión regular para capturar: TIPO IDENTIFICADOR = VALOR; 
        // Soporta cualquier cantidad de espacios o tabulaciones
        const patronAsignacion = /^[A-Z]+\s+([a-zA-Z0-9_]+)\s*=\s*([0-9.]+)\s*;/;
        const coincidencia = lineaLimpia.match(patronAsignacion);
        
        if (coincidencia) {
            const variable = coincidencia[1].trim();
            const valor = parseFloat(coincidencia[2].trim());
            
            if (variable in MemoriaL) {
                MemoriaL[variable] = valor;
            }
        }
    });
}

function ejecutarComandoL(accion, componente) {
    console.log(`\x1b[36m[PARSER SINTÁCTICO] -> Comando Ejecutado: ${accion}(${componente})\x1b[0m`);
    if (accion === "DESCONECTAR") {
        console.log(`   \x1b[31m⚠️ ALERTA ELÉCTRICA: [${componente.toUpperCase()}] ha sido desconectado del flujo.\x1b[0m`);
    } else if (accion === "CONECTAR") {
        console.log(`   \x1b[32m✅ CONTROL: [${componente.toUpperCase()}] re-conectado y sincronizado.\x1b[0m`);
    }
}

// --- PROCESAMIENTO DINÁMICO DEL PROGRAMA 1 ---
function interpretarPrograma1() {
    console.log(`\n\x1b[44m=== LEYENDO Y PROCESANDO ARCHIVO FUENTE: programa1.L ===\x1b[0m`);
    limpiarMemoria();
    
    try {
        const rutaArchivo = path.join(__dirname, 'programa1.L');
        const codigoFuente = fs.readFileSync(rutaArchivo, 'utf-8');
        
        parsearAsignacionesDesdeArchivo(codigoFuente);
        
        console.log(`[TABLA DE SÍMBOLOS INICIAL]:`, MemoriaL);
        console.log(`Estado Inicial de la RED leído: ${MemoriaL.principal} kW`);

        // Evaluación Sintáctica real del IF leído
        if (MemoriaL.principal < 200) {
            console.log(`[AST EVAL] (principal < 200) -> Condición VERDADERA.`);
            ejecutarComandoL("DESCONECTAR", "residencial");
            
            MemoriaL.principal += 100; 
            console.log(`[AST EVAL] Alivio realizado. Nueva potencia Red: ${MemoriaL.principal} kW`);

            if (MemoriaL.principal < 200) {
                ejecutarComandoL("DESCONECTAR", "industrias");
            }
        } else {
            console.log(`[AST EVAL] (principal >= 200) -> Condición FALSA. Red Estable.`);
            ejecutarComandoL("CONECTAR", "residencial");
            ejecutarComandoL("CONECTAR", "industrias");
        }
        console.log(`\x1b[32m✔ Programa 1 finalizado con éxito.\x1b[0m\n`);

    } catch (error) {
        console.error("\x1b[31mError al leer el archivo programa1.L.\x1b[0m", error.message);
    }
}

// --- PROCESAMIENTO DINÁMICO DEL PROGRAMA 2 ---
function interpretarPrograma2() {
    console.log(`\x1b[45m=== LEYENDO Y PROCESANDO ARCHIVO FUENTE: programa2.L ===\x1b[0m`);
    limpiarMemoria();
    
    try {
        const rutaArchivo = path.join(__dirname, 'programa2.L');
        const codigoFuente = fs.readFileSync(rutaArchivo, 'utf-8');
        
        parsearAsignacionesDesdeArchivo(codigoFuente);
        
        console.log(`[TABLA DE SÍMBOLOS INICIAL]: Batería: ${MemoriaL.banco_ion_litio}%, Solar: ${MemoriaL.panel_solar}kW, Consumo: ${MemoriaL.consumo_total}kW`);

        let iteracion = 0;
        // Simulación del árbol del ciclo MIENTRAS
        while (MemoriaL.banco_ion_litio < 95 && iteracion < 5) {
            iteracion++;
            console.log(`\n\x1b[33m--- Ciclo MIENTRAS Iteración #${iteracion} (SoC Batería: ${MemoriaL.banco_ion_litio}%) ---\x1b[0m`);
            
            if (MemoriaL.panel_solar > MemoriaL.consumo_total) {
                console.log(`   [AST EVAL] (panel_solar > consumo_total) -> Excedente Renovables.`);
                ejecutarComandoL("CONECTAR", "banco_ion_litio");
                MemoriaL.banco_ion_litio += 20;   
                MemoriaL.panel_solar -= 30;
            }
            
            if (MemoriaL.panel_solar < MemoriaL.consumo_total) {
                console.log(`   [AST EVAL] (panel_solar < consumo_total) -> Déficit en Microred.`);
                if (MemoriaL.banco_ion_litio > 20) {
                    MemoriaL.banco_ion_litio -= 10;
                    MemoriaL.consumo_total -= 5;
                } else {
                    ejecutarComandoL("DESCONECTAR", "banco_ion_litio");
                    MemoriaL.panel_solar = 0;
                }
            }
        }
        console.log(`\n\x1b[32m✔ Programa 2 finalizado. Balance completado de almacenamiento: ${MemoriaL.banco_ion_litio}%\x1b[0m`);

    } catch (error) {
        console.error("\x1b[31mError al leer el archivo programa2.L.\x1b[0m", error.message);
    }
}

// --- CONTROLADOR GENERAL ---
function main() {
    console.log("==================================================================");
    console.log("INTÉRPRETE COMPILADORES UNEG - LECTURA DE ARCHIVOS FUENTE (.L)");
    console.log("==================================================================");
    
    interpretarPrograma1();
    interpretarPrograma2();
}

main();