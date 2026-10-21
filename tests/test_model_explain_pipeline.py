import numpy as np

from pacote.explain.occlusion import occlusion_explain
from pacote.models.lstm import LSTMRegressor
from pacote.synthetic.driver_response import generate_driver_response_scenario


def test_lstm_regressor_trains_and_predicts():
    scenario = generate_driver_response_scenario(
        n_samples=256,
        lag=4,
        coupling=1.3,
        noise=0.05,
        event_threshold=0.9,
        seed=0,
    )

    model = LSTMRegressor(input_size=1, hidden_size=8, num_layers=1, learning_rate=1e-2)
    X = scenario.driver.reshape(-1, 1)
    y = scenario.response.reshape(-1, 1)

    model.fit(X, y, epochs=5, batch_size=32)
    pred = model.predict(X[:32])

    assert pred.shape == (32, 1)
    assert np.isfinite(pred).all()


def test_occlusion_explainer_returns_attributes():
    scenario = generate_driver_response_scenario(
        n_samples=128,
        lag=3,
        coupling=1.2,
        noise=0.02,
        event_threshold=0.85,
        seed=1,
    )

    attrs = occlusion_explain(
        values=scenario.driver,
        baseline=np.mean(scenario.driver),
        window_size=5,
        model=lambda x: np.abs(x),
    )

    assert attrs.shape == scenario.driver.shape
    assert np.isfinite(attrs).all()
    assert np.abs(attrs).sum() >= 0.0
