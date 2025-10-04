"""Versión refactorizada y eficiente del simulador de dados."""

from __future__ import annotations

import argparse
import cProfile
import io
import timeit
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pstats
import unittest


try:  # pragma: no cover - fallback para line_profiler en entornos sin la librería
	profile  # type: ignore[name-defined]
except NameError:  # pragma: no cover
	def profile(func):  # type: ignore
		return func


FACES = np.arange(1, 7)


@dataclass
class PlayerStats:
	player_id: int
	total_points: int
	frequencies: Dict[int, int]
	most_common_value: int

	def probability_distribution(self) -> Dict[int, float]:
		total_rolls = sum(self.frequencies.values())
		if total_rolls == 0:
			return {face: 0.0 for face in range(1, 7)}
		return {
			face: self.frequencies.get(face, 0) / total_rolls
			for face in range(1, 7)
		}


@dataclass
class GameStatistics:
	total_rounds: int
	players: List[PlayerStats]
	winner: PlayerStats

	def to_dict(self) -> Dict[str, object]:
		return {
			"total_rounds": self.total_rounds,
			"players": [
				{
					"player_id": p.player_id,
					"total_points": p.total_points,
					"frequencies": p.frequencies,
					"most_common_value": p.most_common_value,
				}
				for p in self.players
			],
			"winner": {
				"player_id": self.winner.player_id,
				"total_points": self.winner.total_points,
			},
		}


def _validate_inputs(num_players: int, num_rounds: int, batch_size: int) -> None:
	if not 1 <= num_players <= 4:
		raise ValueError("El número de jugadores debe estar entre 1 y 4")
	if num_rounds <= 0:
		raise ValueError("Las rondas deben ser mayores a cero")
	if batch_size <= 0:
		raise ValueError("El tamaño de lote debe ser mayor a cero")


@profile
def simulate_dice_game(
	num_players: int,
	num_rounds: int,
	*,
	batch_size: int = 100_000,
	seed: int | None = None,
) -> GameStatistics:
	"""Simula un juego de dados vectorizado usando lotes."""

	_validate_inputs(num_players, num_rounds, batch_size)

	rng = np.random.default_rng(seed)
	totals = np.zeros(num_players, dtype=np.int64)
	frequencies = np.zeros((num_players, 6), dtype=np.int64)

	rounds_remaining = num_rounds
	while rounds_remaining > 0:
		current_batch = min(batch_size, rounds_remaining)
		rolls = rng.integers(1, 7, size=(current_batch, num_players), endpoint=False)
		totals += rolls.sum(axis=0)
		for player_idx in range(num_players):
			counts = np.bincount(rolls[:, player_idx], minlength=7)[1:]
			frequencies[player_idx] += counts
		rounds_remaining -= current_batch

	player_stats: List[PlayerStats] = []
	for player_idx in range(num_players):
		freq_dict = {int(face): int(count) for face, count in zip(FACES, frequencies[player_idx])}
		most_common_value = int(np.argmax(frequencies[player_idx]) + 1)
		player_stats.append(
			PlayerStats(
				player_id=player_idx + 1,
				total_points=int(totals[player_idx]),
				frequencies=freq_dict,
				most_common_value=most_common_value,
			)
		)

	winner = max(player_stats, key=lambda p: p.total_points)
	return GameStatistics(total_rounds=num_rounds, players=player_stats, winner=winner)


def simulate_probabilities(
	num_players: int,
	num_rounds: int,
	*,
	batch_size: int = 100_000,
	seed: int | None = None,
) -> Dict[int, Dict[int, float]]:
	stats = simulate_dice_game(num_players, num_rounds, batch_size=batch_size, seed=seed)
	return {player.player_id: player.probability_distribution() for player in stats.players}


def benchmark_simulator(
	num_players: int,
	num_rounds: int,
	*,
	batch_size: int = 100_000,
	repeat: int = 3,
	number: int = 1,
) -> List[float]:
	timer = timeit.Timer(lambda: simulate_dice_game(num_players, num_rounds, batch_size=batch_size))
	return timer.repeat(repeat=repeat, number=number)


def profile_with_cprofile(num_players: int, num_rounds: int, *, batch_size: int = 100_000) -> str:
	profiler = cProfile.Profile()
	profiler.enable()
	simulate_dice_game(num_players, num_rounds, batch_size=batch_size)
	profiler.disable()
	buffer = io.StringIO()
	stats = pstats.Stats(profiler, stream=buffer)
	stats.sort_stats("cumtime")
	stats.print_stats(15)
	return buffer.getvalue()


class DiceGameTests(unittest.TestCase):
	def test_rolls_within_range(self) -> None:
		stats = simulate_dice_game(4, 2_000, batch_size=500, seed=42)
		for player in stats.players:
			for face in player.frequencies.keys():
				self.assertGreaterEqual(face, 1)
				self.assertLessEqual(face, 6)

	def test_probability_sum_is_one(self) -> None:
		probabilities = simulate_probabilities(3, 50_000, batch_size=10_000, seed=123)
		for distribution in probabilities.values():
			self.assertAlmostEqual(sum(distribution.values()), 1.0, places=3)


def run_tests() -> None:
	suite = unittest.defaultTestLoader.loadTestsFromTestCase(DiceGameTests)
	unittest.TextTestRunner(verbosity=2).run(suite)


def main() -> None:
	parser = argparse.ArgumentParser(description="Simulador de dados refactorizado")
	parser.add_argument("--players", type=int, default=4, help="Número de jugadores (1-4)")
	parser.add_argument("--rounds", type=int, default=1_000_000, help="Número de rondas a simular")
	parser.add_argument("--batch", type=int, default=100_000, help="Tamaño de lote")
	parser.add_argument("--seed", type=int, default=None, help="Semilla opcional para reproducibilidad")
	parser.add_argument("--run-tests", action="store_true", help="Ejecuta los tests unitarios")
	parser.add_argument("--profile", action="store_true", help="Ejecuta cProfile sobre la simulación")
	parser.add_argument("--timeit", action="store_true", help="Ejecuta mediciones con timeit")
	args = parser.parse_args()

	if args.run_tests:
		run_tests()
		return

	if args.profile:
		print(profile_with_cprofile(args.players, args.rounds, batch_size=args.batch))

	if args.timeit:
		print(benchmark_simulator(args.players, args.rounds, batch_size=args.batch))

	stats = simulate_dice_game(args.players, args.rounds, batch_size=args.batch, seed=args.seed)
	print(stats.to_dict())


if __name__ == "__main__":
	main()
