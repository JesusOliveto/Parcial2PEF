# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # Ruta al directorio raíz del proyecto

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Proyecto 7 - Simulacion de un Juego de Dados'
copyright = '2025, Olavarria-Lopez'
author = 'Olavarria-Lopez'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [  'sphinx.ext.autodoc',
                'sphinx.ext.viewcode',
                'sphinx.ext.napoleon',
            ]

# TEMA Y ESTILOS
html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']

# Opciones del tema
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

# Configuración específica para autodoc
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

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
