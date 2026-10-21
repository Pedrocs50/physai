import numpy as np

from pacote.evaluate.fidelity import compute_pointing_game, compute_rma
from pacote.synthetic.driver_response import generate_driver_response_scenario


def test_generate_driver_response_scenario():
    scenario = generate_driver_response_scenario(
        n_samples=256,
        lag=4,
        coupling=1.3,
        noise=0.05,
        event_threshold=0.9,
    )

    assert len(scenario.driver) == 256
    assert len(scenario.response) == 256
    assert scenario.causal_mask.shape == (256,)
    assert scenario.event_mask.shape == (256,)
    assert scenario.causal_mask.sum() > 0
    assert scenario.event_mask.sum() > 0


def test_fidelity_metrics():
    scenario = generate_driver_response_scenario(
        n_samples=256,
        lag=4,
        coupling=1.5,
        noise=0.01,
        event_threshold=0.85,
    )

    explanation = np.zeros_like(scenario.driver, dtype=float)
    explanation[scenario.causal_mask] = 1.0

    rma = compute_rma(explanation, scenario.causal_mask)
    pointing_game = compute_pointing_game(explanation, scenario.causal_mask)

    assert 0.0 <= rma <= 1.0
    assert pointing_game in {0.0, 1.0}
