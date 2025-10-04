"""Versión sin refactorizar del simulador de dados.

Esta versión está plagada de malos olores deliberados para el parcial:
- Código duplicado en exceso.
- Uso de variables globales y estado compartido.
- Falta de separación de responsabilidades.
- Simulaciones ineficientes que recalculan información constantemente.
"""

from __future__ import annotations

import argparse
import cProfile
import io
import math  # BAD SMELL: import sobrante que nunca se usa.
import random
import time
import timeit
import pstats
from collections import Counter
from typing import Dict, List, Optional  # BAD SMELL: Optional tampoco se usa.
import unittest


# Fallback para line_profiler cuando no está instalado.
try:  # pragma: no cover - este bloque sólo se ejecuta si falta line_profiler
	profile  # type: ignore[name-defined]
except NameError:  # pragma: no cover
	def profile(func):  # type: ignore
		return func


# BAD SMELL: estado global compartido sin encapsulación.
GLOBAL_RESULTS: Dict[str, List[int]] = {}
GLOBAL_CONFIG = {"ultima_simulacion": None}
GLOBAL_LOG = []  # BAD SMELL: colección global que nunca se limpia.
VALORES_POSIBLES = [1, 2, 3, 4, 5, 6]
TEXTO_FORMATO = "{}"  # BAD SMELL: constante inútil.


def _reiniciar_global(players: int) -> None:
	"""Reinicia el estado global para cada jugador."""

	# BAD SMELL: efectos secundarios escondidos, la función modifica variables globales.
	GLOBAL_RESULTS.clear()
	GLOBAL_CONFIG["ultima_simulacion"] = time.time()
	if players >= 1:
		GLOBAL_RESULTS["player_1"] = []
	if players >= 2:
		GLOBAL_RESULTS["player_2"] = []
	if players >= 3:
		GLOBAL_RESULTS["player_3"] = []
	if players >= 4:
		GLOBAL_RESULTS["player_4"] = []
	GLOBAL_LOG.append(f"reset:{players}")  # BAD SMELL: log global sin límites.


def _tirada_lenta() -> int:
	"""Genera una tirada lenta a propósito."""

	# BAD SMELL: latencia artificial fija (número mágico) que arruina el rendimiento real.
	time.sleep(0.01)
	return random.choice(VALORES_POSIBLES)


# BAD SMELL: comentario sin espacio y redundante, evidencia de poco cuidado.
#Funciones de simulación para cada jugador (código duplicado).

def _simular_jugador1(rondas: int) -> List[int]:  # BAD SMELL: duplicación de código.
	"""Simula las tiradas del jugador 1 con lógica repetida."""
	resultados = []
	for _ in range(rondas):
		resultados.append(_tirada_lenta())
	return resultados


def _simular_jugador2(rondas: int) -> List[int]:  # BAD SMELL: más duplicación.
	"""Simula las tiradas del jugador 2 repitiendo el mismo algoritmo."""
	resultados = []
	for _ in range(rondas):
		resultados.append(_tirada_lenta())
	return resultados


def _simular_jugador3(rondas: int) -> List[int]:  # BAD SMELL: más duplicación.
	"""Simula las tiradas del jugador 3 reutilizando código copiado."""
	resultados = []
	for _ in range(rondas):
		resultados.append(_tirada_lenta())
	return resultados


def _simular_jugador4(rondas: int) -> List[int]:  # BAD SMELL: más duplicación.
	"""Simula las tiradas del jugador 4 con lógica idéntica a los demás."""
	resultados = []
	for _ in range(rondas):
		resultados.append(_tirada_lenta())
	return resultados


def _estadisticas_individuales(nombre: str, tiradas: List[int]) -> Dict[str, object]:
	# BAD SMELL: lógica de formateo mezclada con cálculo.
	"""Calcula estadísticas básicas para un jugador dado.

	Args:
		nombre: Identificador del jugador.
		tiradas: Lista con las tiradas capturadas.

	Returns:
		Diccionario con métricas agregadas.
	"""
	contador = Counter(tiradas)
	total = sum(tiradas)
	if contador:
		mas_frecuente = max(contador.items(), key=lambda x: (x[1], x[0]))[0]
	else:
		mas_frecuente = None
	# BAD SMELL: diccionario sin tipar, mezcla datos y presentación.
	return {
		"jugador": nombre,
		"tiradas": len(tiradas),
		"frecuencias": dict(sorted(contador.items())),
		"total": total,
		"valor_mas_frecuente": mas_frecuente,
		"mensaje": TEXTO_FORMATO.format(f"Jugador {nombre} obtuvo {total} puntos"),  # BAD SMELL: uso de constante trivial.
	}


def _determinar_ganador(estadisticas: List[Dict[str, object]]) -> Dict[str, object]:
	"""Devuelve el jugador con mayor puntaje agregado."""

	# BAD SMELL: la función depende de estructura frágil del diccionario.
	if not estadisticas:
		raise ValueError("No hay jugadores para determinar un ganador")
	ganador = max(estadisticas, key=lambda item: item["total"])
	return {"jugador": ganador["jugador"], "total": ganador["total"]}


def guardar_en_cache(resultado: Dict[str, object], cache: Dict[str, object] = {}) -> None:
	"""Almacena la simulación en una cache global."""

	# BAD SMELL: argumento mutable por defecto + cambio silencioso de estado global.
	cache["ultimo"] = resultado
	GLOBAL_CONFIG["cache"] = cache


@profile  # BAD SMELL: decorador aplicado directamente a función larga.
def simular_juego_sin_refactor(players: int, rondas: int) -> Dict[str, object]:
	"""Ejecuta la simulación principal utilizando el código sin refactorizar."""
	if players < 1 or players > 4:
		raise ValueError("El número de jugadores debe estar entre 1 y 4")
	if rondas <= 0:
		raise ValueError("Las rondas deben ser mayores a cero")

	_reiniciar_global(players)

	if players >= 1:
		GLOBAL_RESULTS["player_1"] = _simular_jugador1(rondas)
	if players >= 2:
		GLOBAL_RESULTS["player_2"] = _simular_jugador2(rondas)
	if players >= 3:
		GLOBAL_RESULTS["player_3"] = _simular_jugador3(rondas)
	if players >= 4:
		GLOBAL_RESULTS["player_4"] = _simular_jugador4(rondas)

	estadisticas = []
	if players >= 1:
		estadisticas.append(_estadisticas_individuales("player_1", GLOBAL_RESULTS["player_1"]))
	if players >= 2:
		estadisticas.append(_estadisticas_individuales("player_2", GLOBAL_RESULTS["player_2"]))
	if players >= 3:
		estadisticas.append(_estadisticas_individuales("player_3", GLOBAL_RESULTS["player_3"]))
	if players >= 4:
		estadisticas.append(_estadisticas_individuales("player_4", GLOBAL_RESULTS["player_4"]))

	try:  # BAD SMELL: captura genérica que oculta errores reales.
		guardar_en_cache({"jugadores": estadisticas, "rondas": rondas})
	except Exception:
		pass

	ganador = _determinar_ganador(estadisticas)
	resultado = {
		"jugadores": estadisticas,
		"total_rondas": rondas,
		"ganador": ganador,
	}
	GLOBAL_LOG.append(resultado)  # BAD SMELL: crecimiento infinito de logs en memoria.
	return resultado


def simular_en_batches_sin_refactor(players: int, rondas: int, batch_size: int = 1000) -> Dict[str, object]:
	"""Aplica la versión ineficiente de batching acumulando tiradas manualmente."""
	if batch_size <= 0:
		raise ValueError("El tamaño de lote debe ser mayor a cero")

	_reiniciar_global(players)
	acumulado: Dict[str, List[int]] = {clave: [] for clave in GLOBAL_RESULTS.keys()}
	rondas_pendientes = rondas
	while rondas_pendientes > 0:
		tamanio = batch_size
		if rondas_pendientes < batch_size:
			tamanio = rondas_pendientes

		resultado = simular_juego_sin_refactor(players, tamanio)
		for jugador in resultado["jugadores"]:
			nombre = jugador["jugador"]
			acumulado.setdefault(nombre, [])
			acumulado[nombre].extend([int(valor) for valor in jugador["frecuencias"].keys() for _ in range(jugador["frecuencias"][valor])])

		rondas_pendientes -= tamanio

	for nombre, valores in acumulado.items():
		GLOBAL_RESULTS[nombre] = valores

	estadisticas = []  # BAD SMELL: acumulador mutable pasado por referencia.
	if players >= 1:
		estadisticas.append(_estadisticas_individuales("player_1", GLOBAL_RESULTS.get("player_1", [])))
	if players >= 2:
		estadisticas.append(_estadisticas_individuales("player_2", GLOBAL_RESULTS.get("player_2", [])))
	if players >= 3:
		estadisticas.append(_estadisticas_individuales("player_3", GLOBAL_RESULTS.get("player_3", [])))
	if players >= 4:
		estadisticas.append(_estadisticas_individuales("player_4", GLOBAL_RESULTS.get("player_4", [])))

	try:
		guardar_en_cache({"batch": True, "jugadores": estadisticas})
	except Exception:
		pass

	ganador = _determinar_ganador(estadisticas)
	return {
		"jugadores": estadisticas,
		"total_rondas": rondas,
		"ganador": ganador,
	}


def perfil_con_cprofile(players: int, rondas: int) -> str:
	"""Ejecuta cProfile sobre la versión sin refactorizar y devuelve el resultado textual."""

	# BAD SMELL: función depende de E/S para efectos secundarios (prints) en lugar de retornar datos puros.
	profiler = cProfile.Profile()
	profiler.enable()
	simular_juego_sin_refactor(players, rondas)
	profiler.disable()
	stream = io.StringIO()
	stats = pstats.Stats(profiler, stream=stream)  # type: ignore[name-defined]
	stats.sort_stats("cumtime")
	stats.print_stats(10)
	return stream.getvalue()



def benchmark_timeit(players: int, rondas: int, repeticiones: int = 3, numero: int = 1) -> List[float]:
	"""Mide tiempos de ejecución usando timeit sobre la versión sin refactorizar."""

	temporizador = timeit.Timer(lambda: simular_juego_sin_refactor(players, rondas))
	return temporizador.repeat(repeat=repeticiones, number=numero)


class TestSimuladorSinRefactor(unittest.TestCase):
	"""Pruebas básicas para validar la implementación sin refactorizar."""

	# BAD SMELL: tests en el mismo archivo que la implementación.
	def test_tirada_en_rango(self) -> None:
		for _ in range(100):
			valor = _tirada_lenta()
			self.assertGreaterEqual(valor, 1)
			self.assertLessEqual(valor, 6)

	def test_probabilidades_sumadas(self) -> None:
		random.seed(123)
		resultado = simular_juego_sin_refactor(2, 500)
		for jugador in resultado["jugadores"]:
			total_tiradas = sum(jugador["frecuencias"].values())
			probabilidades = [conteo / total_tiradas for conteo in jugador["frecuencias"].values() if total_tiradas]
			self.assertAlmostEqual(sum(probabilidades), 1.0, delta=0.05)


def ejecutar_tests() -> None:
	"""Ejecuta las pruebas unitarias asociadas a esta versión."""

	# BAD SMELL: función que sólo reenvía la llamada, añade complejidad innecesaria.
	suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSimuladorSinRefactor)
	unittest.TextTestRunner(verbosity=2).run(suite)


def main() -> None:
	"""Punto de entrada de la aplicación sin refactorizar."""

	parser = argparse.ArgumentParser(description="Simulador de dados sin refactorizar")
	parser.add_argument("--jugadores", type=int, default=4, help="Número de jugadores (1-4)")
	parser.add_argument("--rondas", type=int, default=1000, help="Número de rondas por simulación")
	parser.add_argument("--batch", type=int, default=1000, help="Tamaño de lote para simulaciones en batch")
	parser.add_argument("--run-tests", action="store_true", help="Ejecuta los tests unitarios")
	parser.add_argument("--profile", action="store_true", help="Ejecuta cProfile y muestra las 10 funciones con mayor tiempo acumulado")
	parser.add_argument("--timeit", action="store_true", help="Ejecuta mediciones con timeit")
	args = parser.parse_args()

	if args.run_tests:
		ejecutar_tests()
		return

	if args.profile:
		print(perfil_con_cprofile(args.jugadores, args.rondas))
		GLOBAL_CONFIG["profile_ejecutado"] = True  # BAD SMELL: bandera global escrita desde la capa de UI.

	if args.timeit:
		resultados = benchmark_timeit(args.jugadores, args.rondas)
		print(f"Resultados timeit: {resultados}")

	# BAD SMELL: impresión directa desde la función principal sin separar presentación.
	print("Simulación completa:")
	print(simular_juego_sin_refactor(args.jugadores, args.rondas))
	print("Simulación en lotes (ineficiente):")
	print(simular_en_batches_sin_refactor(args.jugadores, args.rondas, args.batch))


if __name__ == "__main__":
	main()
