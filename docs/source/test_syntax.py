import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

print("=== DIAGNÓSTICO CodigoSinRefactorizar ===")
print("Directorio:", os.path.abspath('../..'))
print("Archivos Python:", [f for f in os.listdir(os.path.abspath('../..')) if f.endswith('.py')])

# Probar si el archivo tiene errores de sintaxis
try:
    with open('../../CodigoSinRefactorizar.py', 'r', encoding='utf-8') as f:
        content = f.read()
    print("✅ Archivo se puede leer")
except Exception as e:
    print(f"❌ No se puede leer archivo: {e}")

# Probar importación
try:
    import CodigoSinRefactorizar
    print("✅ Módulo importado correctamente")
    print("Funciones:", [x for x in dir(CodigoSinRefactorizar) if not x.startswith('_')])
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")