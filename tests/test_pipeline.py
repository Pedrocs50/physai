import numpy as np

from pacote.pipeline import run_benchmark, run_benchmark_suite


def test_run_benchmark_returns_expected_fields():
    result = run_benchmark(
        n_samples=128,
        lag=3,
        coupling=1.1,
        noise=0.05,
        event_threshold=0.85,
        seed=7,
    )

    assert "scenario" in result
    assert "model" in result
    assert "explanation" in result
    assert "metrics" in result
    assert "summary" in result
    assert isinstance(result["scenario"]["event_count"], int)
    assert isinstance(result["metrics"]["rma"], float)
    assert np.isfinite(result["metrics"]["rma"])


def test_run_benchmark_suite_handles_multiple_scenarios():
    result = run_benchmark_suite(
        scenarios=("driver_response", "pulse_response"),
        n_samples=64,
        lag=2,
        coupling=1.0,
        noise=0.05,
        event_threshold=0.85,
        seed=3,
        epochs=2,
    )

    assert isinstance(result["results"], list)
    assert len(result["results"]) == 2
    assert "average_metrics" in result
    assert "average_rma" in result["average_metrics"]
    assert np.isfinite(result["average_metrics"]["average_rma"])
