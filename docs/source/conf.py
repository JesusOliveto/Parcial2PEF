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

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
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
autodoc_mock_imports = [
    'streamlit'
    ]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# Opciones del tema Furo
html_theme_options = {
    "light_css_variables": {
        # Colores principales más suaves
        "color-brand-primary": "#1e40af",
        "color-brand-content": "#1e40af",
        
        # Fondos más claros
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8fafc",
        "color-background-border": "#e2e8f0",
        
        # Sidebar claro
        "color-sidebar-background": "#f1f5f9",
        "color-sidebar-background-border": "#e2e8f0",
        "color-sidebar-caption-text": "#475569",
        "color-sidebar-link-text": "#334155",
        "color-sidebar-item-background": "transparent",
        "color-sidebar-item-background--current": "#dbeafe",
        "color-sidebar-item-text--current": "#1e40af",
        "color-sidebar-item-expander-background": "transparent",
        "color-sidebar-item-expander-background--hover": "#e2e8f0",
        
        # Textos con buen contraste
        "color-foreground-primary": "#1e293b",
        "color-foreground-secondary": "#475569",
        "color-foreground-muted": "#64748b",
        "color-foreground-border": "#cbd5e1",
        
        # Tablas y código
        "color-code-background": "#f1f5f9",
        "color-code-foreground": "#1e293b",
        "color-toc-background": "#ffffff",
    },
    "dark_css_variables": {
        # Versión oscura más suave
        "color-brand-primary": "#60a5fa",
        "color-brand-content": "#60a5fa",
        "color-background-primary": "#0f172a",
        "color-background-secondary": "#1e293b",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_button": "arrow",
    "announcement": "<em>Documentación del Simulador de Dados</em>",
}

# -- CSS PERSONALIZADO MEJORADO --
html_css_files = [
    'custom.css'
]

todo_include_todos = True

def setup(app):
    print("=== SETUP COMPLETADO ===")