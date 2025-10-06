# Proyecto 7 – Simulación de un Juego de Dados

Este proyecto recopila dos implementaciones de un simulador de dados para 1 a 4 jugadores:

1. `CodigoSinRefactorizar.py`: versión con "bad smells" deliberados (duplicación de código, uso excesivo de estado global, batching ineficiente) utilizada como punto de partida para analizar y refactorizar.
2. `CodigoRefactorizado.py`: versión optimizada que aplica buenas prácticas, vectoriza los cálculos con NumPy y deja listas utilidades de profiling y tests.
3. `ImplementacionRefactorizadoStreamlit.py`: interfaz web con Streamlit que consume la versión refactorizada y permite experimentar con los parámetros del simulador.

## Requisitos

Instala las dependencias necesarias (usa PowerShell en Windows):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`line_profiler` se instala junto al resto para poder ejecutar `kernprof`.

## Uso de la versión sin refactorizar

```powershell
python CodigoSinRefactorizar.py --jugadores 4 --rondas 5000 --batch 1000
```

Parámetros útiles:

- `--run-tests`: ejecuta los tests unitarios embebidos.
- `--profile`: lanza `cProfile` y muestra las 10 funciones con mayor tiempo acumulado.
- `--timeit`: calcula tiempos medios con `timeit`.

## Uso de la versión refactorizada

```powershell
python CodigoRefactorizado.py --players 4 --rounds 1000000 --batch 100000 --timeit
```

Argumentos adicionales:

- `--run-tests`: ejecuta la batería de tests optimizados.
- `--profile`: imprime el reporte de `cProfile` ordenado por tiempo acumulado.
- `--timeit`: devuelve mediciones repetidas con `timeit`.
- `--seed`: fija una semilla para reproducibilidad.

Ejemplo de ejecución de `line_profiler`:

```powershell
kernprof -l -v CodigoRefactorizado.py --players 4 --rounds 200000
```

## Interfaz Streamlit

```powershell
streamlit run ImplementacionRefactorizadoStreamlit.py
```

El panel lateral permite ajustar número de jugadores, rondas, tamaño de lote y semilla opcional. Tras pulsar **Simular** se muestran las estadísticas por jugador y métricas globales.

## Tests unitarios

Ambas implementaciones incluyen suites de `unittest` que validan:

- Que las tiradas siempre estén en el rango `[1, 6]`.
- Que la suma de probabilidades por jugador se aproxime a 1.

```powershell
python CodigoSinRefactorizar.py --run-tests
python CodigoRefactorizado.py --run-tests
```

## Perfilado y benchmarks

- **cProfile**: `python CodigoRefactorizado.py --profile`
- **timeit**: `python CodigoRefactorizado.py --timeit`
- **line_profiler**: `kernprof -l -v CodigoRefactorizado.py`

El script refactorizado ejecuta todo el cálculo por lotes en NumPy, por lo que es ideal para estudiar el ahorro respecto de la versión inicial y recoger mediciones objetivas.

# Documentación con Sphinx

Este proyecto incluye documentación profesional generada automáticamente usando **Sphinx** con el tema **Furo** para una experiencia de lectura óptima.

## Generar la Documentación

### Prerrequisitos
Asegúrate de tener instaladas las dependencias de documentación:

```powershell
pip install sphinx furo sphinx-autodoc sphinx-napoleon
```

### Comandos para generar la documentación

```powershell
# Navegar al directorio de documentación
cd docs\source

# Generar archivos .rst automáticamente
sphinx-apidoc -o . .. --force

# Construir la documentación HTML
sphinx-build -b html . _build/html

# Abrir la documentación generada
start _build/html/index.html
```

## Tema y Estilos

### Tema Furo
Hemos configurado **Furo** como tema principal por sus ventajas:
- Diseño moderno y limpio
- Navegación intuitiva con sidebar sticky
- Modo oscuro/claro integrado
- Excelente legibilidad en todos los dispositivos

### Características de la documentación

- **Documentación automática**: Extrae automáticamente docstrings de todos los módulos
- **Búsqueda integrada**: Busca en toda la documentación instantáneamente
- **Diseño responsive**: Se adapta a desktop, tablet y móvil
- **Navegación jerárquica**: Estructura clara de módulos y funciones

## Estructura de la Documentación

```
docs/source/
├── conf.py              # Configuración de Sphinx
├── index.rst            # Página principal
├── modules.rst          # Índice de módulos automático
├── codigo_refactorizado.rst # Documentación específica
├── _static/
│   └── custom.css       # Estilos personalizados
└── _build/html/
    ├── index.html       # Documentación generada
    └── ...              # Archivos estáticos y navegación
```

## Secciones de la Documentación

### 1. Página Principal
- Descripción general del proyecto
- Características principales
- Guía de inicio rápido
- Navegación estructurada

### 2. Módulos Documentados
- `CodigoRefactorizado.py`: Implementación optimizada con NumPy
- `CodigoSinRefactorizar.py`: Versión original para comparación
- `implementacionRefactorizadoStreamlit.py`: Interfaz web con Streamlit

### 3. Documentación Automática
Cada módulo incluye:
- Descripciones de clases y sus métodos
- Parámetros documentados con tipos y descripciones
- Ejemplos de uso integrados
- Herencia y relaciones entre clases

## Personalización

### Modificar estilos
Edita `docs/source/_static/custom.css` para personalizar:

```css
/* Ejemplo de personalización */
body {
    font-family: 'Segoe UI', sans-serif;
}

.sig {
    background-color: #f8f9fa;
    border-left: 4px solid #3498db;
}
```

### Configuración avanzada
Ajusta `docs/source/conf.py` para:
- Cambiar el tema (`html_theme`)
- Agregar extensiones Sphinx
- Modificar opciones de autodoc
- Personalizar metadatos del proyecto

## Características Técnicas

### Extensiones Habilitadas
- `sphinx.ext.autodoc`: Documentación automática desde docstrings
- `sphinx.ext.viewcode`: Enlaces al código fuente
- `sphinx.ext.napoleon`: Soporte para docstrings Google-style
- `sphinx.ext.napoleon`: Índices y búsqueda

### Configuración de Autodoc
```python
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
```

## Acceso a la Documentación

Una vez generada, la documentación está disponible en:
```
file:./docs/source/_build/html/index.html
```

Puedes compartir la carpeta `_build/html/` completa o hospedarla en cualquier servidor web.

---

**Nota**: La documentación se regenera automáticamente cada vez que se modifica el código fuente, manteniéndose siempre actualizada con la implementación actual.