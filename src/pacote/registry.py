"""Registro central de plugins e extensões do projeto."""

from __future__ import annotations

REGISTRY: dict[str, list[str]] = {
    "synthetic": [],
    "data": [],
    "methods": [],
    "models": [],
    "explain": [],
    "evaluate": [],
    "report": [],
}


def register(kind: str, name: str) -> None:
    """Registra um plugin em um conjunto de extensões."""
    if kind not in REGISTRY:
        raise KeyError(f"Tipo de registro desconhecido: {kind}")
    REGISTRY[kind].append(name)
