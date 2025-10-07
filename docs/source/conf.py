# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # Ruta al directorio raíz del proyecto

# -- DIAGNÓSTICO --
print("=== DIAGNÓSTICO SPHINX ===")
print("sys.path:", sys.path)
print("Directorio actual:", os.path.abspath('.'))
print("Directorio raíz:", os.path.abspath('../..'))

try:
    import CodigoSinRefactorizar
    print("✅ Sphinx PUEDE importar CodigoSinRefactorizar")
    print("Funciones:", [x for x in dir(CodigoSinRefactorizar) if not x.startswith('_')])
except Exception as e:
    print(f"❌ Sphinx NO puede importar CodigoSinRefactorizar: {e}")

try:
    import CodigoRefactorizado
    print("✅ Sphinx PUEDE importar CodigoRefactorizado")
except Exception as e:
    print(f"❌ Sphinx NO puede importar CodigoRefactorizado: {e}")
# -- FIN DIAGNÓSTICO --

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Proyecto 7 - Simulacion de un Juego de Dados'
copyright = '2025, Olavarria-Lopez'
author = 'Olavarria-Lopez'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Configuración específica para autodoc --
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'special-members': '__init__',
    'show-inheritance': True,
    'exclude-members': '__weakref__'
}

# Para incluir docstrings de __init__
autoclass_content = 'both'

# Asegurar que no hay imports mockeados que interfieran
autodoc_mock_imports = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# ⚠️ ELIMINÉ LA DUPLICACIÓN - Solo un html_theme
html_theme = 'furo'

html_static_path = ['_static']
html_css_files = ['custom.css']

# Opciones del tema Furo (corregidas)
html_theme_options = {
    # "sidebar_hide_name": False,  # ⚠️ Esta opción puede no existir en Furo
    "navigation_with_keys": True,
}

# -- SETUP FINAL --
def setup(app):
    print("=== SETUP COMPLETADO ===")