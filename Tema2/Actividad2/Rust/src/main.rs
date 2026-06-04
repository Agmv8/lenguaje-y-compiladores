use std::time::Instant;

fn main() {
    println!("=== BENCHMARK: CONJETURA DE COLLATZ (n = 100) ===");
    
    let n = 100;
    let inicio = Instant::now();
    
    for i in 1..=n {
        let mut numero = i;
        while numero > 1 {
            if numero % 2 == 0 {
                numero /= 2;
            } else {
                numero = numero * 3 + 1;
            }
        }
    }
    
    let duracion = inicio.elapsed();
    
    println!("------------------------------------------------");
    println!("¡Demostración completada con éxito para todos los números!");
    println!("Tiempo de procesamiento: {:.4} ms ({:?})", duracion.as_secs_f64() * 1000.0, duracion);
}