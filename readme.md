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
