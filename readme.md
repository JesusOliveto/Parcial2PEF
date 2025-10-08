
# Proyecto 7 – Simulación de un Juego de Dados

Este proyecto recopila dos implementaciones de un simulador de dados para 1 a 4 jugadores:

1. `CodigoSinRefactorizar.py`: versión con *bad smells* deliberados (duplicación de código, estado global, batching ineficiente) usada como base para análisis y refactorización.
2. `CodigoRefactorizado.py`: versión optimizada que aplica buenas prácticas, vectoriza los cálculos con **NumPy** y expone utilidades de *profiling* y *tests*.
3. `ImplementacionRefactorizadoStreamlit.py`: interfaz web con **Streamlit** que consume la versión refactorizada y permite experimentar con los parámetros del simulador.

---

## Requisitos

> Sugerido: Python 3.10+ (probado con 3.13).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- Incluye `line_profiler` para poder ejecutar `kernprof`.
- Para la documentación, instala Sphinx y el tema Furo:
  ```powershell
  pip install sphinx furo
  ```

---

## Uso de la versión **sin refactorizar**

```powershell
python CodigoSinRefactorizar.py --jugadores 4 --rondas 5000 --batch 1000
```

Parámetros útiles:
- `--run-tests`: ejecuta los tests unitarios embebidos.
- `--profile`: lanza `cProfile` y muestra las 10 funciones con mayor tiempo acumulado.
- `--timeit`: calcula tiempos medios con `timeit`.

## Uso de la versión **refactorizada**

```powershell
python CodigoRefactorizado.py --players 4 --rounds 1000000 --batch 100000 --timeit
```

Argumentos adicionales:
- `--run-tests`: ejecuta la batería de tests optimizados.
- `--profile`: imprime el reporte de `cProfile` ordenado por tiempo acumulado.
- `--timeit`: devuelve mediciones repetidas con `timeit`.
- `--seed`: fija una semilla para reproducibilidad.

Ejemplo de `line_profiler`:
```powershell
kernprof -l -v CodigoRefactorizado.py --players 4 --rounds 200000
```

---

## Interfaz Streamlit

```powershell
streamlit run ImplementacionRefactorizadoStreamlit.py
```
El panel lateral permite ajustar número de jugadores, rondas, tamaño de lote y semilla. Tras pulsar **Simular** se muestran estadísticas por jugador y métricas globales.

---

## Tests unitarios

Ambas implementaciones incluyen suites de `unittest` que validan:
- Que las tiradas siempre estén en el rango `[1, 6]`.
- Que la suma de probabilidades por jugador se aproxime a 1.

```powershell
python CodigoSinRefactorizar.py --run-tests
python CodigoRefactorizado.py --run-tests
```

---

## Resultados de *profiling* y benchmarks (ejecuciones reales)

### `line_profiler` (kernprof)
| Versión | Función | Tiempo total |
|---|---|---|
| Sin refactor | `simular_juego_sin_refactor` | **83.88180 s** |
| Refactorizada | `simulate_dice_game` | **0.19532 s** |

**Speedup ≈ ×429.46**

<details>
<summary>Fragmento relevante (sin refactor): cuello de botella</summary>

```
4000   41.701    0.010   41.701    0.010 {built-in method time.sleep}
```
</details>

### `cProfile`
| Versión | Tiempo total | Comentario |
|---|---:|---|
| Sin refactor | **41.805 s** | Dominado por `time.sleep` en `_tirada_lenta` |
| Refactorizada | **0.172 s** | Vectorización + batching |

**Speedup ≈ ×243.05**

### `timeit` (3 corridas)
| Versión | Corridas (s) | Promedio |
|---|---|---:|
| Sin refactor | 41.956, 41.755, 41.631 | **41.780 s** |
| Refactorizada | 0.178, 0.166, 0.159 | **0.168 s** |

**Speedup ≈ ×249.07**

> **Conclusión:** La versión sin refactor está limitada por una espera artificial de 10 ms por tirada (`time.sleep`). La versión refactorizada elimina esa latencia y utiliza generación vectorizada de tiradas + acumulación por lotes, logrando mejoras entre ×243 y ×429 según la herramienta.

---

## Documentación con Sphinx

Este proyecto incluye documentación generada con **Sphinx** y tema **Furo**.

### Generar documentación

```powershell
# Navegar al directorio de documentación
cd docs\source

# Generar archivos .rst
sphinx-apidoc -o . .. --force

# Construir la documentación HTML
sphinx-build -b html . _build/html

# Abrir la documentación generada
start _build/html/index.html
```

### Estructura de la documentación

```
docs/source/
├── conf.py                  # Configuración de Sphinx
├── index.rst                # Página principal
├── modules.rst              # Índice de módulos automático
├── codigo_refactorizado.rst # Documentación específica
├── _static/
│   └── custom.css           # Estilos personalizados
└── _build/html/
    └── index.html           # Documentación generada
```

### Extensiones (conf.py)

```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
html_theme = "furo"
```

---

## Notas de refactorización (resumen)

- **Duplicación →** *Replace Method with Parameter* + **vectorización**: una sola función `simulate_dice_game(...)` para 1–4 jugadores.
- **Estado global →** *Encapsulate Collection* + *Replace Global with Objects*: uso de `PlayerStats` y `GameStatistics`.
- **Latencia artificial →** eliminar `time.sleep(...)` y generar tiradas en bloques con `numpy.random.Generator.integers`.
- **Batching real →** acumular totales y frecuencias por lote (`batch_size`) en lugar de re-simular.
- **Validaciones →** `_validate_inputs` asegura límites y tamaños.
- **Tests** cubren rango de tiradas y distribución de probabilidades.

