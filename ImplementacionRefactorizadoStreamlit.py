"""Aplicación Streamlit con juego interactivo y simulador batch."""

from __future__ import annotations

import random
import time
from typing import Iterable, List

import streamlit as st

from CodigoRefactorizado import GameStatistics, PlayerStats, simulate_dice_game


ASCII_DICE = {
	1: (
		"┌─────┐",
		"│     │",
		"│  ●  │",
		"│     │",
		"└─────┘",
	),
	2: (
		"┌─────┐",
		"│●    │",
		"│     │",
		"│    ●│",
		"└─────┘",
	),
	3: (
		"┌─────┐",
		"│●    │",
		"│  ●  │",
		"│    ●│",
		"└─────┘",
	),
	4: (
		"┌─────┐",
		"│●   ●│",
		"│     │",
		"│●   ●│",
		"└─────┘",
	),
	5: (
		"┌─────┐",
		"│●   ●│",
		"│  ●  │",
		"│●   ●│",
		"└─────┘",
	),
	6: (
		"┌─────┐",
		"│●   ●│",
		"│●   ●│",
		"│●   ●│",
		"└─────┘",
	),
}


def _ensure_state() -> None:
	st.session_state.setdefault("vista", "juego")
	st.session_state.setdefault("scores", [0, 0, 0, 0])
	st.session_state.setdefault("round", 0)
	st.session_state.setdefault("history", [])
	st.session_state.setdefault("last_faces", [1, 1, 1, 1])


def _dice_art(face: int) -> str:
	caras = ASCII_DICE[face]
	return "```\n" + "\n".join(caras) + "\n```"


def _animate_roll(placeholders: Iterable[st.delta_generator.DeltaGenerator], final_faces: List[int]) -> None:
	for _ in range(8):
		for idx, placeholder in enumerate(placeholders):
			placeholder.markdown(_dice_art(random.randint(1, 6)))
		time.sleep(0.08)
	for idx, placeholder in enumerate(placeholders):
		placeholder.markdown(_dice_art(final_faces[idx]))


def _reset_game() -> None:
	st.session_state["scores"] = [0, 0, 0, 0]
	st.session_state["round"] = 0
	st.session_state["history"] = []
	st.session_state["last_faces"] = [1, 1, 1, 1]


def _render_scoreboard() -> None:
	score_data = [
		{"Jugador": idx + 1, "Puntos": st.session_state["scores"][idx]}
		for idx in range(4)
	]
	st.subheader("Marcador acumulado")
	st.table(score_data)


def _render_history() -> None:
	if not st.session_state["history"]:
		st.info("Aún no hay rondas jugadas.")
		return

	st.subheader("Historial de rondas")
	st.dataframe(st.session_state["history"], use_container_width=True)


def _render_game_view() -> None:
	st.title("Juego de Dados Multijugador")
	st.caption("Cuatro jugadores se turnan lanzando dados con animación ASCII.")

	cols = st.columns(4)
	placeholders = []
	for idx, col in enumerate(cols):
		col.markdown(f"**Jugador {idx + 1}**")
		placeholder = col.empty()
		placeholder.markdown(_dice_art(st.session_state["last_faces"][idx]))
		placeholders.append(placeholder)

	st.markdown(f"### Ronda actual: {st.session_state['round']}")
	if st.button("Lanzar dados 🎲"):
		final_faces = [random.randint(1, 6) for _ in range(4)]
		_animate_roll(placeholders, final_faces)
		st.session_state["last_faces"] = final_faces
		st.session_state["round"] += 1
		for idx, face in enumerate(final_faces):
			st.session_state["scores"][idx] += face
		st.session_state["history"].append(
			{"Ronda": st.session_state["round"], **{f"J{idx + 1}": face for idx, face in enumerate(final_faces)}}
		)
		st.success(
			" | ".join(
				[
					f"Jugador {idx + 1}: {face} puntos (total {st.session_state['scores'][idx]})"
					for idx, face in enumerate(final_faces)
				]
			)
		)

	_reset_col, _ = st.columns([1, 3])
	with _reset_col:
		if st.button("Reiniciar partida", type="secondary"):
			_reset_game()
			st.experimental_rerun()

	_render_scoreboard()
	_render_history()


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


def _mostrar_resultados(stats: GameStatistics) -> None:
	st.subheader("Resumen de la simulación masiva")
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


def _render_simulator_view() -> None:
	st.title("Simulador en Batches (versión refactorizada)")
	st.markdown(
		"""
		Configura los parámetros y ejecuta la simulación vectorizada para comparar con el juego manual.
		"""
	)

	num_players = st.slider("Número de jugadores", min_value=1, max_value=4, value=4)
	num_rounds = st.number_input(
		"Número de rondas", min_value=1, max_value=5_000_000, value=1_000_000, step=50_000
	)
	batch_size = st.number_input(
		"Tamaño de lote", min_value=1, max_value=1_000_000, value=100_000, step=10_000
	)
	seed_value = st.number_input("Semilla (opcional)", min_value=0, value=0, step=1)
	usar_semilla = st.checkbox("Usar semilla fija", value=False)

	if st.button("Ejecutar simulación masiva"):
		st.write("Calculando...")
		seed = int(seed_value) if usar_semilla else None
		stats = simulate_dice_game(
			num_players,
			int(num_rounds),
			batch_size=int(batch_size),
			seed=seed,
		)
		_mostrar_resultados(stats)
		st.success("Simulación completada. Explora las estadísticas en los desplegables.")

	st.info(
		"Para perfiles detallados, ejecuta los scripts de consola descritos en `readme.md`."
	)


def main() -> None:
	_ensure_state()
	st.sidebar.title("Panel de control")
	st.sidebar.markdown("Selecciona qué vista quieres usar.")

	if st.sidebar.button("Ir al simulador masivo"):
		st.session_state["vista"] = "simulacion"
	if st.sidebar.button("Volver al juego multijugador"):
		st.session_state["vista"] = "juego"

	st.sidebar.markdown("---")
	st.sidebar.write(f"Vista actual: **{st.session_state['vista'].capitalize()}**")
	st.sidebar.markdown(
		"""
		**Consejos rápidos:**

		- `python CodigoRefactorizado.py --profile`
		- `kernprof -l -v CodigoRefactorizado.py`
		- `python CodigoRefactorizado.py --timeit`
		"""
	)

	if st.session_state["vista"] == "simulacion":
		_render_simulator_view()
	else:
		_render_game_view()


if __name__ == "__main__":
	main()
