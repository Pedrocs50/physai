from __future__ import annotations

import numpy as np


def compute_rma(explanation: np.ndarray, causal_mask: np.ndarray) -> float:
    """Massa de relevância: fração da explicação contida na máscara causal."""
    explanation = np.asarray(explanation, dtype=float)
    causal_mask = np.asarray(causal_mask, dtype=bool)
    if explanation.shape != causal_mask.shape:
        raise ValueError("explicação e máscara devem ter a mesma forma")
    total = float(np.abs(explanation).sum())
    if total == 0:
        return 0.0
    return float(np.abs(explanation[causal_mask]).sum() / total)


def compute_pointing_game(explanation: np.ndarray, causal_mask: np.ndarray) -> float:
    """Pointing game: retorna 1.0 se o maior valor cai na região causal."""
    explanation = np.asarray(explanation, dtype=float)
    causal_mask = np.asarray(causal_mask, dtype=bool)
    if explanation.shape != causal_mask.shape:
        raise ValueError("explicação e máscara devem ter a mesma forma")
    if not causal_mask.any():
        return 0.0
    max_idx = int(np.argmax(explanation))
    return 1.0 if causal_mask[max_idx] else 0.0
