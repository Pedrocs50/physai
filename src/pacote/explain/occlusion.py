from __future__ import annotations

import numpy as np


def occlusion_explain(
    values: np.ndarray,
    baseline: float | np.ndarray,
    window_size: int = 5,
    model=None,
) -> np.ndarray:
    """Explicação por oclusão simples: mede a mudança de saída ao remover uma janela."""
    values = np.asarray(values, dtype=float)
    if values.ndim != 1:
        raise ValueError("values deve ser unidimensional")
    if window_size < 1:
        raise ValueError("window_size deve ser >= 1")

    if model is None:
        model = lambda x: np.abs(x)

    baseline_value = np.asarray(baseline, dtype=float)
    if baseline_value.ndim == 0:
        baseline_array = np.full_like(values, float(baseline_value))
    else:
        baseline_array = np.asarray(baseline, dtype=float)
        if baseline_array.shape != values.shape:
            raise ValueError("baseline deve ter a mesma forma de values")

    original = model(values)
    attributions = np.zeros_like(values, dtype=float)

    for i in range(len(values)):
        start = max(0, i - window_size // 2)
        end = min(len(values), i + window_size // 2 + 1)
        masked = values.copy()
        masked[start:end] = baseline_array[start:end]
        modified = model(masked)
        attributions[i] = float(np.abs(original - modified).sum())

    return attributions
