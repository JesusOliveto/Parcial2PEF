"""Aplicación Streamlit que usa la versión refactorizada del simulador."""

from __future__ import annotations

import streamlit as st

from CodigoRefactorizado import GameStatistics, PlayerStats, simulate_dice_game


def _formatear_probabilidades(jugador: PlayerStats) -> list[dict[str, float]]:
	distribucion = jugador.probability_distribution()
	return [
		{
			"cara": face,
			"frecuencia": jugador.frequencies.get(face, 0),
			"probabilidad": round(distribucion.get(face, 0.0), 5),
		}
		for face in range(1, 7)
	]


def mostrar_resultados(stats: GameStatistics) -> None:
	st.subheader("Resumen del juego")
	st.metric("Rondas totales", stats.total_rounds)
	st.metric(
		"Ganador",
		f"Jugador {stats.winner.player_id}",
		help=f"Total acumulado: {stats.winner.total_points}",
	)

	for jugador in stats.players:
		with st.expander(f"Jugador {jugador.player_id}"):
			st.write(f"Puntos totales: {jugador.total_points}")
			st.write(f"Valor más frecuente: {jugador.most_common_value}")
			st.table(_formatear_probabilidades(jugador))


def main() -> None:
	st.title("Simulador de Juego de Dados (versión refactorizada)")
	st.markdown(
		"""
		Ajusta los parámetros a continuación y presiona **Simular** para ejecutar la
		versión optimizada del simulador en lotes.
		"""
	)

	with st.sidebar:
		st.header("Parámetros de simulación")
		num_players = st.slider("Número de jugadores", min_value=1, max_value=4, value=3)
		num_rounds = st.number_input(
			"Número de rondas", min_value=1, max_value=5_000_000, value=1_000_000, step=50_000
		)
		batch_size = st.number_input(
			"Tamaño de lote", min_value=1, max_value=1_000_000, value=100_000, step=10_000
		)
		seed_value = st.number_input("Semilla (opcional)", min_value=0, value=0, step=1)
		usar_semilla = st.checkbox("Usar semilla", value=False)

	if st.button("Simular"):
		st.write("Ejecutando simulación...")
		seed = int(seed_value) if usar_semilla else None
		stats = simulate_dice_game(
			num_players,
			int(num_rounds),
			batch_size=int(batch_size),
			seed=seed,
		)
		mostrar_resultados(stats)

		st.success("Simulación completada. Revisa los detalles en cada jugador.")

	st.sidebar.markdown("---")
	st.sidebar.markdown(
		"""
		**Consejos:**

		- Ejecuta `python CodigoRefactorizado.py --profile` para ver cProfile.
		- Ejecuta `kernprof -l -v CodigoRefactorizado.py` para usar line_profiler.
		- Usa `python CodigoRefactorizado.py --timeit` para mediciones rápidas con timeit.
		"""
	)


if __name__ == "__main__":
	main()
