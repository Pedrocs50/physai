from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class DriverResponseScenario:
    """Estrutura mínima de um cenário sintético com verdade conhecida."""

    driver: np.ndarray
    response: np.ndarray
    causal_mask: np.ndarray
    event_mask: np.ndarray
    lag: int
    coupling: float
    noise: float
    scenario_name: str = "driver_response"


def generate_driver_response_scenario(
    n_samples: int = 256,
    lag: int = 4,
    coupling: float = 1.5,
    noise: float = 0.05,
    event_threshold: float = 0.9,
    seed: int | None = None,
) -> DriverResponseScenario:
    """Gera um cenário sintético simples com driver, resposta e máscara causal."""
    rng = np.random.default_rng(seed)

    driver = np.cumsum(rng.normal(0.0, 1.0, size=n_samples))
    driver = (driver - driver.mean()) / (driver.std() + 1e-8)

    response = np.zeros(n_samples, dtype=float)
    for i in range(lag, n_samples):
        response[i] = 0.7 * response[i - 1] + 0.2 * driver[i - lag] + rng.normal(0.0, noise)

    response = response + coupling * driver

    event_mask = response >= np.quantile(response, event_threshold)
    causal_mask = np.zeros(n_samples, dtype=bool)
    for idx in np.where(event_mask)[0]:
        start = max(0, idx - lag)
        end = min(n_samples, idx + 1)
        causal_mask[start:end] = True

    return DriverResponseScenario(
        driver=driver,
        response=response,
        causal_mask=causal_mask,
        event_mask=event_mask,
        lag=lag,
        coupling=coupling,
        noise=noise,
        scenario_name="driver_response",
    )


def generate_pulse_response_scenario(
    n_samples: int = 256,
    lag: int = 4,
    coupling: float = 1.0,
    noise: float = 0.05,
    event_threshold: float = 0.9,
    seed: int | None = None,
) -> DriverResponseScenario:
    """Gera um cenário com respostas impulsivas, útil para benchmark multi-cenário."""
    rng = np.random.default_rng(seed)

    time = np.arange(n_samples, dtype=float)
    base = np.sin(2.0 * np.pi * time / max(12, n_samples // 3))
    pulse_positions = rng.choice(np.arange(n_samples), size=max(3, n_samples // 20), replace=False)
    pulse_pattern = np.zeros(n_samples, dtype=float)
    for pos in pulse_positions:
        pulse_pattern[max(0, pos - lag): min(n_samples, pos + lag + 1)] += coupling * (1.0 - np.abs(np.arange(-lag, lag + 1)) / max(1, lag + 1))

    driver = base + 0.15 * rng.normal(size=n_samples)
    driver = (driver - driver.mean()) / (driver.std() + 1e-8)

    response = 0.6 * np.roll(driver, 1) + 0.3 * driver + pulse_pattern + rng.normal(0.0, noise, size=n_samples)
    response = response + 0.25 * np.sin(2.0 * np.pi * time / (n_samples / 6.0))

    event_mask = np.abs(response) >= np.quantile(np.abs(response), event_threshold)
    causal_mask = np.zeros(n_samples, dtype=bool)
    for idx in np.where(event_mask)[0]:
        start = max(0, idx - lag)
        end = min(n_samples, idx + lag + 1)
        causal_mask[start:end] = True

    return DriverResponseScenario(
        driver=driver,
        response=response,
        causal_mask=causal_mask,
        event_mask=event_mask,
        lag=lag,
        coupling=coupling,
        noise=noise,
        scenario_name="pulse_response",
    )


SCENARIO_GENERATORS: dict[str, callable] = {
    "driver_response": generate_driver_response_scenario,
    "pulse_response": generate_pulse_response_scenario,
}


def generate_scenario(name: str, **kwargs) -> DriverResponseScenario:
    """Cria um cenário sintético pelo nome registrado."""
    if name not in SCENARIO_GENERATORS:
        available = ", ".join(sorted(SCENARIO_GENERATORS))
        raise ValueError(f"Cenário desconhecido: {name}. Disponíveis: {available}")
    return SCENARIO_GENERATORS[name](**kwargs)
