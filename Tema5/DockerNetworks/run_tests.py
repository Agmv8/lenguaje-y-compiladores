import os
import sys
from docker_networks_parser import analizar_archivo_yaml

def run_all_tests():
    dir_base = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(dir_base, 'test_files')
    
    archivos_prueba = [
        ('1. Válido Básico', 'docker-compose-valid1.yml'),
        ('2. Válido 
         (IPAM/IPv6)', 'docker-compose-valid2.yml'),
        ('3. Error Léxico (Carácter Inválido)', 'docker-compose-invalid-lexical.yml'),
        ('4. Error Sintáctico (Modo Pánico / Recuperación)', 'docker-compose-invalid-syntax.yml')
    ]
    
    print("=" * 70)
    print(" EJECUTANDO PRUEBAS DEL PARSER DE REDES DOCKER (MIEMBRO 3)")
    print("=" * 70)
    
    exitos = 0
    totales = len(archivos_prueba)
    
    for desc, nombre in archivos_prueba:
        ruta = os.path.join(test_dir, nombre)
        print(f"\n>>> Prueba: {desc}")
        resultado = analizar_archivo_yaml(ruta)
        if resultado:
            exitos += 1
            
    print("\n" + "=" * 70)
    print(f" RESUMEN DE PRUEBAS:")
    print(f"  Total de pruebas: {totales}")
    print(f"  Exitosas (Sin errores o recuperadas con éxito): {exitos}/{totales}")
    print("=" * 70)

if __name__ == "__main__":
    run_all_tests()
