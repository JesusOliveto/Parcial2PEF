"""Aplicación Streamlit con juego interactivo y simulador batch."""

from __future__ import annotations

import random
import time
from typing import Callable, Iterable, List, Optional

import streamlit as st

from CodigoRefactorizado import GameStatistics, PlayerStats, simulate_dice_game


ASCII_DICE = {
	1: (
		"┌─────────┐",
		"│         │",
		"│    ●    │",
		"│         │",
		"└─────────┘",
	),
	2: (
		"┌─────────┐",
		"│ ●       │",
		"│         │",
		"│       ● │",
		"└─────────┘",
	),
	3: (
		"┌─────────┐",
		"│  ●      │",
		"│    ●    │",
		"│      ●  │",
		"└─────────┘",
	),
	4: (
		"┌─────────┐",
		"│  ●   ●  │",
		"│         │",
		"│  ●   ●  │",
		"└─────────┘",
	),
	5: (
		"┌─────────┐",
		"│  ●   ●  │",
		"│    ●    │",
		"│  ●   ●  │",
		"└─────────┘",
	),
	6: (
		"┌─────────┐",
		"│  ●   ●  │",
		"│  ●   ●  │",
		"│  ●   ●  │",
		"└─────────┘",
	),
}


def _ensure_state() -> None:
	"""Inicializa las claves necesarias dentro de ``st.session_state``."""

	st.session_state.setdefault("vista", "juego")
	st.session_state.setdefault("scores", [0, 0, 0, 0])
	st.session_state.setdefault("round", 0)
	st.session_state.setdefault("history", [])
	st.session_state.setdefault("last_faces", [1, 1, 1, 1])
	st.session_state.setdefault("finished", False)
	st.session_state.setdefault("winner_info", None)


def _safe_rerun() -> None:
	"""Intenta relanzar la app usando la API disponible (estable o experimental)."""

	rerun_fn: Optional[Callable[[], None]] = getattr(st, "rerun", None)
	if rerun_fn is None:
		rerun_fn = getattr(st, "experimental_rerun", None)
	if rerun_fn is not None:
		rerun_fn()


def _dice_art(face: int) -> str:
	"""Devuelve la representación ASCII de un dado para la cara indicada."""

	caras = ASCII_DICE[face]
	return "```\n" + "\n".join(caras) + "\n```"


def _animate_roll(placeholders: Iterable[st.delta_generator.DeltaGenerator], final_faces: List[int]) -> None:
	"""Muestra una animación de tirada antes de fijar los valores definitivos."""

	for _ in range(8):
		for idx, placeholder in enumerate(placeholders):
			placeholder.markdown(_dice_art(random.randint(1, 6)))
		time.sleep(0.08)
	for idx, placeholder in enumerate(placeholders):
		placeholder.markdown(_dice_art(final_faces[idx]))


def _reset_game() -> None:
	"""Restablece los contadores y últimas caras mostradas."""

	st.session_state["scores"] = [0, 0, 0, 0]
	st.session_state["round"] = 0
	st.session_state["history"] = []
	st.session_state["last_faces"] = [1, 1, 1, 1]
	st.session_state["finished"] = False
	st.session_state["winner_info"] = None


def _render_scoreboard() -> None:
	"""Presenta una tabla con el puntaje acumulado por jugador."""

	score_data = [
		{"Jugador": idx + 1, "Puntos": st.session_state["scores"][idx]}
		for idx in range(4)
	]
	st.subheader("Marcador acumulado")
	st.table(score_data)


def _render_history() -> None:
	"""Muestra el historial de rondas jugadas o un aviso si aún no hay datos."""

	if not st.session_state["history"]:
		st.info("Aún no hay rondas jugadas.")
		return

	st.subheader("Historial de rondas")
	st.dataframe(st.session_state["history"], width="stretch")


def _render_game_view() -> None:
	"""Renderiza la vista principal del juego interactivo de dados."""

	st.title("Juego de Dados Multijugador")

	cols = st.columns(4)
	placeholders = []
	for idx, col in enumerate(cols):
		col.markdown(f"**Jugador {idx + 1}**")
		placeholder = col.empty()
		placeholder.markdown(_dice_art(st.session_state["last_faces"][idx]))
		placeholders.append(placeholder)

	# FIX: Para evitar que el contador de ronda quede "una por detrás" mostramos el botón primero,
	# procesamos la acción y luego pintamos el encabezado con el valor actualizado.
	lanzar = st.button("Lanzar dados 🎲", disabled=st.session_state.get("finished", False))
	if lanzar and not st.session_state.get("finished", False):
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

	# Mostrar la ronda al usuario iniciando en 1 (evitar mostrar 0 tras reinicio).
	# Internamente 'round' representa rondas completadas; si es 0, se muestra 1 como primera ronda.
	current_round_display = st.session_state["round"] if st.session_state["round"] > 0 else 1
	st.markdown(f"### Ronda actual: {current_round_display}")

	col_actions, _ = st.columns([2, 3])
	with col_actions:
		c1, c2 = st.columns(2)
		with c1:
			if st.button("Reiniciar partida", type="secondary"):
				_reset_game()
				_safe_rerun()
		with c2:
			if st.button("Finalizar juego", disabled=st.session_state.get("finished", False)):
				# Determinar ganador y marcar estado finalizado
				scores = st.session_state["scores"]
				max_score = max(scores)
				winners = [i + 1 for i, sc in enumerate(scores) if sc == max_score]
				st.session_state["finished"] = True
				st.session_state["winner_info"] = {"puntaje": max_score, "ganadores": winners}

	# Mostrar panel de ganador si el juego fue finalizado
	if st.session_state.get("finished", False) and st.session_state.get("winner_info"):
		info = st.session_state["winner_info"]
		ganadores = info["ganadores"]
		if len(ganadores) == 1:
			st.success(f"Juego finalizado. Ganador: Jugador {ganadores[0]} con {info['puntaje']} puntos.")
		else:
			st.warning(
				"Juego finalizado. Empate entre: "
				+ ", ".join(f"Jugador {g}" for g in ganadores)
				+ f" (todos con {info['puntaje']} puntos)."
			)

	_render_scoreboard()
	_render_history()


def _formatear_probabilidades(jugador: PlayerStats) -> list[dict[str, float]]:
	"""Transforma las probabilidades en una estructura tabular para Streamlit."""

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
	"""Despliega las estadísticas producidas por la simulación masiva."""

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
	"""Construye la vista dedicada al simulador vectorizado."""

	st.title("Simulador en Batches")
	st.markdown(
		"""
		Configura los parámetros y ejecuta la simulación vectorizada para comparar con el juego manual.
		"""
	)

	num_players = st.slider("Número de jugadores", min_value=1, max_value=4, value=4)
	num_rounds = st.number_input(
		"Número de rondas", min_value=1, max_value=5_000_000, value=1_000_000, step=50_000,
		help="Cantidad total de tiradas por jugador (mayor cifra = más precisión estadística pero más tiempo)."
	)
	batch_size = st.number_input(
		"Tamaño de lote", min_value=1, max_value=1_000_000, value=100_000, step=10_000,
		help="Número máximo de tiradas procesadas en un bloque. Un valor más alto reduce overhead pero aumenta uso puntual de memoria."
	)
	seed_value = st.number_input(
		"Semilla (opcional)", min_value=0, value=0, step=1,
		help="Fija la semilla para reproducir resultados. Se ignora si no marcas la casilla."
	)
	usar_semilla = st.checkbox("Usar semilla fija", value=False, help="Activa la semilla provista arriba para reproducibilidad.")

	# Avisos dinámicos de validación / recomendación
	# 1. batch mayor que rondas
	if batch_size > num_rounds:
		st.warning(
			f"El tamaño de lote ({batch_size:,}) es mayor que las rondas ({num_rounds:,}). El último bloque será más pequeño; puedes reducir el lote para ser más eficiente."
		)
	# 2. lote demasiado pequeño para muchas rondas
	if num_rounds / batch_size > 500:
		st.info(
			"Estás usando un tamaño de lote muy pequeño respecto al total de rondas. Aumentarlo puede acelerar el cálculo (menos iteraciones de bucle)."
		)
	# 3. sugerencia de tamaño de lote óptimo aproximado
	recommended = min(max(10_000, num_rounds // 10), 100_000)
	if batch_size < recommended and num_rounds > 50_000:
		st.caption(
			f"Sugerencia: un tamaño de lote cercano a {recommended:,} podría equilibrar rendimiento y memoria."
		)
	# 4. cálculo rápido de memoria estimada para el lote máximo
	max_batch_bytes = batch_size * num_players * 8  # int64
	if max_batch_bytes > 5_000_000:  # > ~5 MB
		mb = max_batch_bytes / (1024 * 1024)
		st.caption(
			f"Uso de memoria estimado por lote: {mb:0.2f} MB (num_players × batch_size × 8 bytes)."
		)
	else:
		kb = max_batch_bytes / 1024
		st.caption(
			f"Uso de memoria estimado por lote: {kb:0.1f} KB."
		)
	# 5. semilla
	if not usar_semilla:
		st.caption("Semilla no aplicada: resultados variarán en cada ejecución.")

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
	"""Punto de entrada de Streamlit que alterna entre juego y simulador."""

	_ensure_state()
	st.sidebar.title("Panel de control")
	st.sidebar.markdown("Selecciona qué vista quieres usar.")

	if st.sidebar.button("Ir al simulador masivo"):
		st.session_state["vista"] = "simulacion"
	if st.sidebar.button("Volver al juego multijugador"):
		st.session_state["vista"] = "juego"

	st.sidebar.markdown("---")
	st.sidebar.write(f"Vista actual: **{st.session_state['vista'].capitalize()}**")


	if st.session_state["vista"] == "simulacion":
		_render_simulator_view()
	else:
		_render_game_view()


if __name__ == "__main__":
	main()
