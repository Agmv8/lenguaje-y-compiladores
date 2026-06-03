use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::time::Instant;

// Estructura para el Bloque
#[derive(Debug, Clone)]
struct Bloque {
    id: usize,
    mensaje: String,
    hash_anterior: u64,
    hash_actual: u64,
}

impl Bloque {
    // Función para crear un nuevo bloque y calcular su hash
    fn nuevo(id: usize, mensaje: String, hash_anterior: u64) -> Self {
        let mut bloque = Bloque {
            id,
            mensaje,
            hash_anterior,
            hash_actual: 0,
        };
        bloque.hash_actual = bloque.calcular_hash();
        bloque
    }

    // Calcula el hash combinando el hash anterior y el mensaje actual (hash + mensaje)
    fn calcular_hash(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.hash_anterior.hash(&mut hasher);
        self.mensaje.hash(&mut hasher);
        hasher.finish()
    }
}

fn main() {
    // 1. Tabla con N mensajes fijos
    let tabla_mensajes = vec![
        "Mensaje inicial: Configuración del sistema.".to_string(),
        "Transacción 1: Alejandro envía 10 BTC a Luis.".to_string(),
        "Transacción 2: Carlos registra un nuevo contrato.".to_string(),
        "Transacción 3: Se valida el bloque de datos médicos.".to_string(),
        "Mensaje final: Cierre de la cadena de bloques.".to_string(),
    ];

    let mut blockchain: Vec<Bloque> = Vec::new();
    
    // Medir el tiempo de ejecución (una métrica muy común en Rust)
    let inicio = Instant::now();

    // 2. Creación del Bloque Génesis (el primero, no tiene hash anterior)
    let bloque_genesis = Bloque::nuevo(0, tabla_mensajes[0].clone(), 0);
    blockchain.push(bloque_genesis);

    // 3. Construcción de la cadena uniendo cada bloque con el hash del anterior
    for (i, mensaje) in tabla_mensajes.iter().enumerate().skip(1) {
        let hash_previo = blockchain.last().unwrap().hash_actual;
        let nuevo_bloque = Bloque::nuevo(i, mensaje.clone(), hash_previo);
        blockchain.push(nuevo_bloque);
    }

    let duracion = inicio.elapsed();

    // 4. Mostrar el resultado de la simulación
    println!("=== SIMULACIÓN DE BLOCKCHAIN EN RUST ===");
    for bloque in &blockchain {
        println!("--------------------------------------------------");
        println!("Bloque ID:     {}", bloque.id);
        println!("Mensaje:       \"{}\"", bloque.mensaje);
        println!("Hash Anterior: {:X}", bloque.hash_anterior);
        println!("Hash Actual:   {:X}", bloque.hash_actual);
    }
    println!("--------------------------------------------------");
    
    // 5. Demostración de Integridad (Validación)
    println!("\nVerificando la integridad de la cadena...");
    let mut cadena_valida = true;
    for i in 1..blockchain.len() {
        if blockchain[i].hash_anterior != blockchain[i-1].hash_actual {
            cadena_valida = false;
        }
    }
    
    if cadena_valida {
        println!("✅ ¡La cadena es LEGÍTIMA! Los hashes coinciden perfectamente.");
    } else {
        println!("❌ ¡Alerta! La cadena ha sido manipulada.");
    }

    println!("Tiempo de procesamiento: {:?}", duracion);
}
