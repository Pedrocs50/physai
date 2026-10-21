"""CLI mínima para o benchmark sintético de eventos extremos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from pacote.evaluate.fidelity import compute_pointing_game, compute_rma
from pacote.explain.occlusion import occlusion_explain
from pacote.models.lstm import LSTMRegressor
from pacote.pipeline import run_benchmark, run_benchmark_suite
from pacote.synthetic.driver_response import generate_driver_response_scenario, generate_scenario


def _write_json(payload: dict, output: str | None) -> None:
    if output is None:
        return
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def cmd_synth(args: argparse.Namespace) -> None:
    scenario = generate_driver_response_scenario(
        n_samples=args.n_samples,
        lag=args.lag,
        coupling=args.coupling,
        noise=args.noise,
        event_threshold=args.event_threshold,
        seed=args.seed,
    )
    payload = {
        "n_samples": int(len(scenario.driver)),
        "lag": int(scenario.lag),
        "coupling": float(scenario.coupling),
        "noise": float(scenario.noise),
        "event_count": int(scenario.event_mask.sum()),
        "causal_count": int(scenario.causal_mask.sum()),
        "driver_mean": float(np.mean(scenario.driver)),
        "response_mean": float(np.mean(scenario.response)),
    }
    _write_json(payload, args.output)
    print(json.dumps(payload, indent=2))


def cmd_train(args: argparse.Namespace) -> None:
    scenario = generate_driver_response_scenario(
        n_samples=args.n_samples,
        lag=args.lag,
        coupling=args.coupling,
        noise=args.noise,
        event_threshold=args.event_threshold,
        seed=args.seed,
    )
    X = scenario.driver.reshape(-1, 1)
    y = scenario.response.reshape(-1, 1)
    model = LSTMRegressor(input_size=1, hidden_size=args.hidden_size, num_layers=1, learning_rate=args.lr)
    model.fit(X, y, epochs=args.epochs, batch_size=args.batch_size)
    pred = model.predict(X[-args.batch_size :])
    payload = {
        "n_samples": int(len(X)),
        "epochs": int(args.epochs),
        "pred_shape": list(pred.shape),
        "pred_mean": float(np.mean(pred)),
        "target_mean": float(np.mean(y)),
    }
    _write_json(payload, args.output)
    print(json.dumps(payload, indent=2))


def cmd_explain(args: argparse.Namespace) -> None:
    scenario = generate_driver_response_scenario(
        n_samples=args.n_samples,
        lag=args.lag,
        coupling=args.coupling,
        noise=args.noise,
        event_threshold=args.event_threshold,
        seed=args.seed,
    )
    explanation = occlusion_explain(
        values=scenario.driver,
        baseline=np.mean(scenario.driver),
        window_size=args.window_size,
        model=lambda x: np.abs(x),
    )
    payload = {
        "top_indices": [int(idx) for idx in np.argsort(np.abs(explanation))[-10:]],
        "mean_attribution": float(np.mean(explanation)),
        "max_attribution": float(np.max(explanation)),
    }
    _write_json(payload, args.output)
    print(json.dumps(payload, indent=2))


def cmd_eval(args: argparse.Namespace) -> None:
    scenario = generate_driver_response_scenario(
        n_samples=args.n_samples,
        lag=args.lag,
        coupling=args.coupling,
        noise=args.noise,
        event_threshold=args.event_threshold,
        seed=args.seed,
    )
    explanation = np.zeros_like(scenario.driver, dtype=float)
    explanation[scenario.causal_mask] = 1.0
    payload = {
        "rma": float(compute_rma(explanation, scenario.causal_mask)),
        "pointing_game": float(compute_pointing_game(explanation, scenario.causal_mask)),
    }
    _write_json(payload, args.output)
    print(json.dumps(payload, indent=2))


def cmd_report(args: argparse.Namespace) -> None:
    scenario = generate_driver_response_scenario(
        n_samples=args.n_samples,
        lag=args.lag,
        coupling=args.coupling,
        noise=args.noise,
        event_threshold=args.event_threshold,
        seed=args.seed,
    )
    explanation = np.zeros_like(scenario.driver, dtype=float)
    explanation[scenario.causal_mask] = 1.0
    payload = {
        "summary": {
            "event_count": int(scenario.event_mask.sum()),
            "causal_count": int(scenario.causal_mask.sum()),
            "rma": float(compute_rma(explanation, scenario.causal_mask)),
            "pointing_game": float(compute_pointing_game(explanation, scenario.causal_mask)),
        }
    }
    _write_json(payload, args.output)
    print(json.dumps(payload, indent=2))


def cmd_run(args: argparse.Namespace) -> None:
    payload = run_benchmark(
        n_samples=args.n_samples,
        lag=args.lag,
        coupling=args.coupling,
        noise=args.noise,
        event_threshold=args.event_threshold,
        seed=args.seed,
        epochs=args.epochs,
        batch_size=args.batch_size,
        hidden_size=args.hidden_size,
        learning_rate=args.lr,
        window_size=args.window_size,
        output_dir=args.output_dir,
        scenario_name=args.scenario,
    )
    print(json.dumps(payload["summary"], indent=2))


def cmd_suite(args: argparse.Namespace) -> None:
    scenarios = tuple(item.strip() for item in args.scenarios.split(",") if item.strip())
    payload = run_benchmark_suite(
        scenarios=scenarios,
        n_samples=args.n_samples,
        lag=args.lag,
        coupling=args.coupling,
        noise=args.noise,
        event_threshold=args.event_threshold,
        seed=args.seed,
        epochs=args.epochs,
        batch_size=args.batch_size,
        hidden_size=args.hidden_size,
        learning_rate=args.lr,
        window_size=args.window_size,
        output_dir=args.output_dir,
    )
    print(json.dumps(payload["average_metrics"], indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="physai", description="Benchmark sintético de IA interpretável para eventos extremos")
    subparsers = parser.add_subparsers(dest="command", required=True)

    synth = subparsers.add_parser("synth", help="Gerar cenário sintético")
    synth.add_argument("--n-samples", type=int, default=256)
    synth.add_argument("--lag", type=int, default=4)
    synth.add_argument("--coupling", type=float, default=1.3)
    synth.add_argument("--noise", type=float, default=0.05)
    synth.add_argument("--event-threshold", type=float, default=0.9)
    synth.add_argument("--seed", type=int, default=0)
    synth.add_argument("--output", type=str, default=None)
    synth.set_defaults(func=cmd_synth)

    train = subparsers.add_parser("train", help="Treinar o modelo LSTM mínimo")
    train.add_argument("--n-samples", type=int, default=256)
    train.add_argument("--lag", type=int, default=4)
    train.add_argument("--coupling", type=float, default=1.3)
    train.add_argument("--noise", type=float, default=0.05)
    train.add_argument("--event-threshold", type=float, default=0.9)
    train.add_argument("--seed", type=int, default=0)
    train.add_argument("--epochs", type=int, default=5)
    train.add_argument("--batch-size", type=int, default=32)
    train.add_argument("--hidden-size", type=int, default=8)
    train.add_argument("--lr", type=float, default=1e-2)
    train.add_argument("--output", type=str, default=None)
    train.set_defaults(func=cmd_train)

    explain = subparsers.add_parser("explain", help="Gerar explicação por oclusão")
    explain.add_argument("--n-samples", type=int, default=256)
    explain.add_argument("--lag", type=int, default=4)
    explain.add_argument("--coupling", type=float, default=1.3)
    explain.add_argument("--noise", type=float, default=0.05)
    explain.add_argument("--event-threshold", type=float, default=0.9)
    explain.add_argument("--seed", type=int, default=0)
    explain.add_argument("--window-size", type=int, default=5)
    explain.add_argument("--output", type=str, default=None)
    explain.set_defaults(func=cmd_explain)

    eval_parser = subparsers.add_parser("eval", help="Avaliar fidelidade da explicação")
    eval_parser.add_argument("--n-samples", type=int, default=256)
    eval_parser.add_argument("--lag", type=int, default=4)
    eval_parser.add_argument("--coupling", type=float, default=1.3)
    eval_parser.add_argument("--noise", type=float, default=0.05)
    eval_parser.add_argument("--event-threshold", type=float, default=0.9)
    eval_parser.add_argument("--seed", type=int, default=0)
    eval_parser.add_argument("--output", type=str, default=None)
    eval_parser.set_defaults(func=cmd_eval)

    report = subparsers.add_parser("report", help="Gerar relatório resumido do cenário")
    report.add_argument("--n-samples", type=int, default=256)
    report.add_argument("--lag", type=int, default=4)
    report.add_argument("--coupling", type=float, default=1.3)
    report.add_argument("--noise", type=float, default=0.05)
    report.add_argument("--event-threshold", type=float, default=0.9)
    report.add_argument("--seed", type=int, default=0)
    report.add_argument("--output", type=str, default=None)
    report.set_defaults(func=cmd_report)

    run = subparsers.add_parser("run", help="Executar o benchmark completo do v0.1")
    run.add_argument("--scenario", type=str, default="driver_response", choices=("driver_response", "pulse_response"))
    run.add_argument("--n-samples", type=int, default=256)
    run.add_argument("--lag", type=int, default=4)
    run.add_argument("--coupling", type=float, default=1.3)
    run.add_argument("--noise", type=float, default=0.05)
    run.add_argument("--event-threshold", type=float, default=0.9)
    run.add_argument("--seed", type=int, default=0)
    run.add_argument("--epochs", type=int, default=5)
    run.add_argument("--batch-size", type=int, default=32)
    run.add_argument("--hidden-size", type=int, default=8)
    run.add_argument("--lr", type=float, default=1e-2)
    run.add_argument("--window-size", type=int, default=5)
    run.add_argument("--output-dir", type=str, default=None)
    run.set_defaults(func=cmd_run)

    suite = subparsers.add_parser("suite", help="Executar o benchmark multi-cenário")
    suite.add_argument("--scenarios", type=str, default="driver_response,pulse_response")
    suite.add_argument("--n-samples", type=int, default=256)
    suite.add_argument("--lag", type=int, default=4)
    suite.add_argument("--coupling", type=float, default=1.3)
    suite.add_argument("--noise", type=float, default=0.05)
    suite.add_argument("--event-threshold", type=float, default=0.9)
    suite.add_argument("--seed", type=int, default=0)
    suite.add_argument("--epochs", type=int, default=5)
    suite.add_argument("--batch-size", type=int, default=32)
    suite.add_argument("--hidden-size", type=int, default=8)
    suite.add_argument("--lr", type=float, default=1e-2)
    suite.add_argument("--window-size", type=int, default=5)
    suite.add_argument("--output-dir", type=str, default=None)
    suite.set_defaults(func=cmd_suite)

    return parser


def main() -> None:
    """Ponto de entrada da CLI do projeto."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
