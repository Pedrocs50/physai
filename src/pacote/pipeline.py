from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from pacote.evaluate.fidelity import compute_pointing_game, compute_rma
from pacote.explain.occlusion import occlusion_explain
from pacote.models.lstm import LSTMRegressor
from pacote.synthetic.driver_response import generate_scenario


def run_benchmark(
    n_samples: int = 256,
    lag: int = 4,
    coupling: float = 1.3,
    noise: float = 0.05,
    event_threshold: float = 0.9,
    seed: int = 0,
    epochs: int = 5,
    batch_size: int = 32,
    hidden_size: int = 8,
    learning_rate: float = 1e-2,
    window_size: int = 5,
    output_dir: str | None = None,
    scenario_name: str = "driver_response",
) -> dict:
    """Executa o benchmark sintético do projeto para um cenário específico."""
    scenario = generate_scenario(
        scenario_name,
        n_samples=n_samples,
        lag=lag,
        coupling=coupling,
        noise=noise,
        event_threshold=event_threshold,
        seed=seed,
    )

    X = scenario.driver.reshape(-1, 1)
    y = scenario.response.reshape(-1, 1)
    model = LSTMRegressor(
        input_size=1,
        hidden_size=hidden_size,
        num_layers=1,
        learning_rate=learning_rate,
    )
    model.fit(X, y, epochs=epochs, batch_size=batch_size)
    prediction = model.predict(X[-batch_size:])

    explanation = occlusion_explain(
        values=scenario.driver,
        baseline=np.mean(scenario.driver),
        window_size=window_size,
        model=lambda x: np.abs(x),
    )

    metrics = {
        "rma": float(compute_rma(explanation, scenario.causal_mask)),
        "pointing_game": float(compute_pointing_game(explanation, scenario.causal_mask)),
    }

    summary = {
        "event_count": int(scenario.event_mask.sum()),
        "causal_count": int(scenario.causal_mask.sum()),
        "rma": metrics["rma"],
        "pointing_game": metrics["pointing_game"],
        "prediction_mean": float(np.mean(prediction)),
    }

    result = {
        "scenario_name": scenario.scenario_name,
        "scenario": {
            "n_samples": int(len(scenario.driver)),
            "lag": int(scenario.lag),
            "coupling": float(scenario.coupling),
            "noise": float(scenario.noise),
            "event_count": int(scenario.event_mask.sum()),
            "causal_count": int(scenario.causal_mask.sum()),
        },
        "model": {
            "epochs": int(epochs),
            "batch_size": int(batch_size),
            "hidden_size": int(hidden_size),
            "learning_rate": float(learning_rate),
            "prediction_shape": list(prediction.shape),
            "prediction_mean": float(np.mean(prediction)),
        },
        "explanation": {
            "window_size": int(window_size),
            "mean_attribution": float(np.mean(explanation)),
            "max_attribution": float(np.max(explanation)),
        },
        "metrics": metrics,
        "summary": summary,
    }

    if output_dir is not None:
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        (path / "benchmark_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    return result


def run_benchmark_suite(
    scenarios: tuple[str, ...] | list[str] | None = None,
    n_samples: int = 256,
    lag: int = 4,
    coupling: float = 1.3,
    noise: float = 0.05,
    event_threshold: float = 0.9,
    seed: int = 0,
    epochs: int = 5,
    batch_size: int = 32,
    hidden_size: int = 8,
    learning_rate: float = 1e-2,
    window_size: int = 5,
    output_dir: str | None = None,
) -> dict:
    """Executa vários cenários sintéticos e agrega métricas médias."""
    names = tuple(scenarios or ("driver_response", "pulse_response"))
    results: list[dict] = []

    for name in names:
        result = run_benchmark(
            n_samples=n_samples,
            lag=lag,
            coupling=coupling,
            noise=noise,
            event_threshold=event_threshold,
            seed=seed,
            epochs=epochs,
            batch_size=batch_size,
            hidden_size=hidden_size,
            learning_rate=learning_rate,
            window_size=window_size,
            output_dir=output_dir,
            scenario_name=name,
        )
        results.append({
            "scenario_name": name,
            "summary": result["summary"],
            "metrics": result["metrics"],
        })

    average_rma = float(np.mean([item["metrics"]["rma"] for item in results]))
    average_pointing_game = float(np.mean([item["metrics"]["pointing_game"] for item in results]))
    payload = {
        "n_scenarios": len(results),
        "scenarios": list(names),
        "results": results,
        "average_metrics": {
            "average_rma": average_rma,
            "average_pointing_game": average_pointing_game,
        },
    }

    if output_dir is not None:
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        (path / "benchmark_suite_summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return payload
