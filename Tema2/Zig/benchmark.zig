const std = @import("std");

const LIMITE: u64 = 1_000_000;

fn collatz_pasos(n: u64) u64 {
    var x: u64 = n;
    var pasos: u64 = 0;
    while (x != 1) {
        if (x % 2 == 0) {
            x = x / 2;
        } else {
            x = 3 * x + 1;
        }
        pasos += 1;
    }
    return pasos;
}

pub fn main() void {
    std.debug.print("=== Benchmarking: Conjetura de Collatz ===\n", .{});
    std.debug.print("Calculando para todos los n < {d}\n\n", .{LIMITE});

    var max_pasos: u64 = 0;
    var n_max_pasos: u64 = 0;
    var i: u64 = 2;

    while (i < LIMITE) : (i += 1) {
        const pasos = collatz_pasos(i);
        if (pasos > max_pasos) {
            max_pasos = pasos;
            n_max_pasos = i;
        }
    }

    std.debug.print("Resultado:\n", .{});
    std.debug.print("  Numero con mas pasos: {d}\n", .{n_max_pasos});
    std.debug.print("  Cantidad de pasos:    {d}\n", .{max_pasos});
}