# diagnosticar_modulo.py en docs/source/
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

print("=== DIAGNÓSTICO ImplementacionRefactorizadoStreamlit ===")

try:
    import ImplementacionRefactorizadoStreamlit as modulo
    print("✅ Módulo importado correctamente")
    
    # Ver qué contiene
    print("🔍 Contenido del módulo:")
    elementos = [x for x in dir(modulo) if not x.startswith('_')]
    if elementos:
        for elem in elementos:
            print(f"   - {elem}")
    else:
        print("   ⚠️ El módulo no tiene elementos públicos (sin _)")
        
    # Verificar si es un script principal
    if hasattr(modulo, '__name__') and modulo.__name__ == '__main__':
        print("⚠️  El archivo está diseñado para ejecutarse como script principal")
        
except Exception as e:
    print(f"❌ Error importando: {e}")