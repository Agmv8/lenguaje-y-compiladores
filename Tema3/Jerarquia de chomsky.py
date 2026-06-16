# Jerarquia_de_chomsky.py — Simulador Visual
# Lenguaje y Compiladores 2026-I | UNEG | Arnaldo Perdomo
import tkinter as tk
from tkinter import ttk, messagebox
import random

class ChomskyVisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Jerarquía de Chomsky - Simulador Visual")
        self.root.geometry("1420x880")
        self.root.configure(bg="#0a1428")

        # Título
        tk.Label(root, text="Jerarquía de Chomsky", font=("Arial", 26, "bold"), 
                fg="#60a5fa", bg="#0a1428").pack(pady=8)
        tk.Label(root, text="Simulador Visual Interactivo • Tema 3 - Lenguaje y Compiladores | UNEG", 
                font=("Arial", 12), fg="#94a3b8", bg="#0a1428").pack()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.create_tab(0, "Tipo 0", "#eab308", "Sin Restricción")
        self.create_tab(1, "Tipo 1", "#8b5cf6", "Sensible al Contexto")
        self.create_tab(2, "Tipo 2", "#22d3ee", "Libre de Contexto")
        self.create_tab(3, "Tipo 3", "#f97316", "Regular")

    def create_tab(self, tipo, num, color, nombre):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=f"{num} — {nombre}")

        # Header
        header = tk.Frame(frame, bg=color, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=f"TIPO {tipo} — {nombre}", 
                font=("Arial", 18, "bold"), bg=color, 
                fg="black" if tipo in [0,2,3] else "white").pack(pady=22)

        main = tk.Frame(frame, bg="#1e2937")
        main.pack(fill="both", expand=True, padx=15, pady=15)

        # Panel Izquierdo - Explicación Detallada
        left = tk.Frame(main, bg="#1e2937", width=580)
        left.pack(side="left", fill="y", padx=(0,15))

        tk.Label(left, text="Explicación y Poder Computacional", 
                font=("Arial", 12, "bold"), bg="#1e2937", fg="white").pack(anchor="w", padx=15, pady=10)

        info = tk.Text(left, height=22, font=("Consolas", 10), bg="#111827", fg="#bae6fd", wrap="word")
        info.pack(fill="both", expand=True, padx=15, pady=5)
        info.insert("1.0", self.get_detailed_info(tipo))
        info.config(state="disabled")

        # Panel Derecho - Prueba Interactiva
        right = tk.Frame(main, bg="#1e2937")
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Prueba el Lenguaje", font=("Arial", 12, "bold"), 
                bg="#1e2937", fg="white").pack(pady=8)

        tk.Label(right, text="Ingresa una cadena:", bg="#1e2937", fg="white").pack(anchor="w", padx=20)
        
        entry = tk.Entry(right, font=("Consolas", 14), width=60, bg="#334155", fg="white", relief="flat")
        entry.pack(pady=8, padx=20)

        btn_frame = tk.Frame(right, bg="#1e2937")
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="Validar", bg="#22d3ee", fg="black", font=("Arial", 10, "bold"), width=12,
                 command=lambda: self.validate(tipo, entry, result)).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Generar Ejemplo", bg="#eab308", fg="black", font=("Arial", 10, "bold"), width=15,
                 command=lambda: self.generate_example(tipo, entry, result)).pack(side="left", padx=8)

        result = tk.Text(right, height=15, font=("Consolas", 11), bg="#0f172a", fg="#67e8f9")
        result.pack(fill="both", expand=True, padx=20, pady=10)

    def get_detailed_info(self, tipo):
        texts = {
            0: "Poder ilimitado\nAutómata: Máquina de Turing\nCapacidad: Lenguajes Recursivamente Enumerables (LRE)\n\nCaracterísticas:\n• No tiene restricciones en las producciones\n• Puede simular cualquier algoritmo\n• No garantiza terminación\n\nEjemplo: Cualquier lenguaje computable.",
            1: "Requiere memoria proporcional a la entrada\nAutómata: Autómata Linealmente Acotado (ALA)\n\nCaracterísticas:\n• Producciones: αAβ → αγβ (|γ| ≥ 1)\n• No puede reducir la longitud de la cadena\n\nEjemplo clásico: { aⁿ bⁿ cⁿ | n ≥ 1 }\nConcordancia gramatical (el gato / los gatos).",
            2: "Memoria en pila (stack)\nAutómata: Autómata de Pila (PDA)\n\nCaracterísticas:\n• Producciones: A → α (A único no-terminal)\n• Ideal para estructuras jerárquicas y recursivas\n\nEjemplos comunes:\n• Paréntesis balanceados\n• Expresiones aritméticas\n• Sintaxis de lenguajes de programación.",
            3: "Memoria constante\nAutómata: Autómata Finito (AFD / AFND)\n\nCaracterísticas:\n• Producciones lineales por derecha o izquierda\n• Muy eficiente (tiempo lineal O(n))\n\nUso principal:\n• Análisis Léxico en compiladores\n• Identificadores, números, palabras clave."
        }
        return texts.get(tipo, "")

    def validate(self, tipo, entry, result):
        cadena = entry.get().strip()
        if not cadena:
            messagebox.showwarning("Atención", "Ingresa una cadena")
            return

        result.delete("1.0", tk.END)
        result.insert("1.0", f"Cadena: {cadena}\n\n")

        if tipo == 3:
            ok = self.is_valid_id(cadena)
            result.insert("end", f"{'✅' if ok else '❌'} TIPO 3 (Regular): {'VÁLIDA' if ok else 'NO VÁLIDA'}\n")
            result.insert("end", "Uso: Análisis Léxico en compiladores")
        elif tipo == 2:
            ok = self.balanced_parentheses(cadena)
            result.insert("end", f"{'✅' if ok else '❌'} TIPO 2 (GLC): {'Paréntesis balanceados' if ok else 'Desbalanceados'}\n")
            result.insert("end", "Común en sintaxis de lenguajes de programación")
        elif tipo == 1:
            ok = self.is_an_bncn(cadena)
            result.insert("end", f"{'✅' if ok else '❌'} TIPO 1 (CSL): {'Válida (aⁿbⁿcⁿ)' if ok else 'No válida'}\n")
            result.insert("end", "Ejemplo clásico de gramática sensible al contexto")
        else:
            result.insert("end", "TIPO 0 (Sin Restricción):\nCualquier cadena es potencialmente aceptable.\nPoder computacional máximo.")

    def generate_example(self, tipo, entry, result):
        examples = {
            0: f"cualquierCadenaValida{random.randint(100,999)}",
            1: "a"*random.randint(3,5) + "b"*random.randint(3,5) + "c"*random.randint(3,5),
            2: "((a + b) * (c - d))",
            3: random.choice(["variable", "total_2026", "nombre_usuario", "sumaFinal", "contador1"])
        }
        ex = examples[tipo]
        entry.delete(0, tk.END)
        entry.insert(0, ex)
        result.delete("1.0", tk.END)
        result.insert("1.0", f"Ejemplo generado (Tipo {tipo}):\n\n{ex}\n\n→ Presiona 'Validar'")

    def is_valid_id(self, s):
        if not s: return False
        if not (s[0].isalpha() or s[0] == '_'): return False
        return all(c.isalnum() or c == '_' for c in s)

    def balanced_parentheses(self, s):
        count = 0
        for c in s:
            if c == '(': count += 1
            elif c == ')': count -= 1
            if count < 0: return False
        return count == 0

    def is_an_bncn(self, s):
        try:
            a, rest = s.split('b', 1)
            b, c = rest.split('c', 1) if 'c' in rest else (rest, '')
            return len(a) == len(b) == len(c) > 0 and a == 'a'*len(a) and b == 'b'*len(b) and c == 'c'*len(c)
        except:
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = ChomskyVisualApp(root)
    root.mainloop()